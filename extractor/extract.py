import asyncio
import re
import time
from io import StringIO

import pandas as pd
from bs4 import BeautifulSoup
from playwright.async_api import Playwright, async_playwright

from . import utility


class Scraper:
    def __init__(self):
        self.year = None
        self.total = 0
        self.result = list()

    async def _get(self, playwright: Playwright, value: str) -> None:
        url = "https://www.portal.oit.ac.jp/CAMJWEB/slbssrch.do"
        dropdown = "select[name='value(crclm)']"
        search_button = "#srch_skgr_search"
        no_result_mark = "font[color='red']"
        next_page = "a:has-text('次の50件>>')"
        text = ""
        video_dir_path = "video/"
        sleep_time = 5
        page_size = 50

        # ブラウザの起動
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(record_video_dir=video_dir_path)

        try:
            # 検索ページを開く
            page = await context.new_page()
            await page.goto(url)
            await page.select_option(dropdown, value)

            # 検索ボタンをクリック
            await page.click(search_button)
            time.sleep(sleep_time)

        except Exception as e:
            print(e)
            return

        else:
            # 検索結果がない場合
            if await page.query_selector(no_result_mark):
                print(f"{utility.department(value)}: 0件")
                return

            # 検索結果を取得
            while not text:
                text = await page.inner_text("body")

            # 件数を取得
            number = int(re.search(r"(\d+)件中", text).group(1))
            print(f"{utility.department(value)}: {str(number)}件")
            self.total += number

            for i in range(number // page_size + 1):
                time.sleep(sleep_time)

                # 検索結果からテーブルを取得
                html = (await page.content()).replace("<br>", "@")
                soup = BeautifulSoup(html, "html.parser")
                table = soup.find_all(class_="list")
                df = (pd.read_html(StringIO(str(table))))[0]

                # 0行目と1行目と一番下の行を削除
                df = df.drop([0, 1, len(df) - 1])
                # 0列目(No)と2列目(講義名)と4列目(担当教員)を削除
                df = df.drop(df.columns[[0, 2, 4]], axis=1)

                # リストに追加
                df_list = df.values.tolist()
                for j in range(len(df_list)):
                    dow, period = utility.dow_period(utility.normalize(df_list[j][1]))
                    self.result.append(
                        [
                            utility.department(value),
                            utility.url(self.year, df_list[j][0]),
                            dow,
                            period
                        ]
                    )

                # ページが分割されており最終ページでない場合、次のページに移動
                if number > page_size and i < number // page_size:
                    await page.click(next_page)

        finally:
            await page.close()
            await context.close()
            await browser.close()

    async def _run(self, value) -> None:
        async with async_playwright() as playwright:
            await self._get(playwright, value)

    def main(self, year: str) -> None:
        self.year = year

        for value in utility.values():
            asyncio.run(self._run(value))
            utility.output(year, self.result)

        print(f"合計: {self.total}件")
