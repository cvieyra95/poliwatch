import { NextResponse } from "next/server";
import * as cheerio from "cheerio";

export async function GET() {
  try {
    const pages = 3
    let trades = []
    for(let page = 1; page <= pages; page++){
       const html = await fetch(`https://www.capitoltrades.com/trades?page=${page}`, {
      headers: {
        "User-Agent": "Mozilla/5.0",
      },
    }).then(res => res.text());

    const $ = cheerio.load(html);
    $("table tbody tr").each((i, el) => {
      const tds = $(el).find("td");

      const name = $(tds[0]).find("a").text().trim();
      const company = $(tds[1]).text().trim();
      const type = $(tds[6]).text().trim();
      const amount = $(tds[7]).text().trim();
      const date = $(tds[3]).text().trim();

      trades.push({
        name,
        company,
        type,
        amount,
        date,
      });
    });

    }

   
    return NextResponse.json(trades);
  } catch (err) {
    console.error(err);
    return NextResponse.json(
      { error: "Failed to scrape trades" },
      { status: 500 }
    );
  }
}
