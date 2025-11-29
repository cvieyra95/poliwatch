// components/Sidebar.js
"use client";
import styles from "./Sidebar.module.css"
import { useState, useEffect } from "react";

export default function Sidebar() {

  const [trades, setTrades] = useState([]);
  useEffect(() => {
      async function fetchTrades() {
        try {
          const response = await fetch("https://127.0.0.0/trades"); //Calls the API and Limits to 15 trades
          const data = await response.json();
          setTrades(data);
        } catch (err) {
          console.error("Error fetching trades:", err);
        }
      }
      fetchTrades();
    }, []);

  return (
    <div className={styles.sidebar}>
      <div className={styles.tradebox}>
        <div className={styles.tradeheader}>
          <h3>Latest Trades</h3>
          <a className={styles.viewall}>Vew All</a>
        </div>
         <table className={styles.table}>
          <thead>
            <tr>
              <th>Name</th>
              <th>Symbol</th>
              <th>Type</th>
              <th>Amount</th>
            </tr>
          </thead>
          <tbody>
            {trades.map((p) => {
              const tradeType = p.trade_type.toLowerCase() === "buy" ? styles.buy : styles.sell
              return (
                <tr className={styles.row} key={p.id}>
                  <td>{p.first_name} {p.last_name}</td>
                  <td className={styles.symbol}><a href={`https://finance.yahoo.com/quote/${p.symbol}`} target="_blank">${p.symbol}</a></td>
                  <td className={`${styles.type} ${tradeType}`}>{p.trade_type}</td>
                  <td>{p.trade_size}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
        
      </div>
    </div>
  );
}