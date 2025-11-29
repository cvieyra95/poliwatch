// app/api/trades/route.js
import { NextResponse } from "next/server";

export async function GET() {
  try {
    const response = await fetch(
      "https://capitoltrades.com/trades",
      {
        headers: {
          "User-Agent": "Mozilla/5.0",
          Accept: "application/json"
        },
      }
    );

    const data = await response.json();
    console.log(data)
    return NextResponse.json(data.data.items);
  } catch (err) {
    return NextResponse.json({ error: "Failed to fetch trades" }, { status: 500 });
  }
}
