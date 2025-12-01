// components/Sidebar.js
"use client";
import styles from "./Sidebar.module.css"
import { useState, useEffect } from "react";
import Link from "next/link";

export default function Sidebar() {

  const [trades, setTrades] = useState([]);
  useEffect(() => {
      async function fetchTrades() {
        try {
          const response = await fetch("/api/trades"); //Calls the API and Limits to 15 trades
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
          <Link className= {styles.viewall}href='/trades'>View all</Link>
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
            {trades.slice(0,15).map((p, index) => {
              const tradeType = p.type.toLowerCase() === "buy" ? styles.buy : styles.sell
              return (
                <tr className={styles.row} key={`${p.name}-${p.company}-${index}`}>
                  <td>{p.name}</td>
                  <td className={styles.symbol}><a href={`https://www.google.com/search?q=${p.company}`} target="_blank">${p.company}</a></td>
                  <td className={`${styles.type} ${tradeType}`}>{p.type.toUpperCase()}</td>

                  <td className={`${styles.type}`}>{p.amount}</td>
                  
                </tr>
              )
            })}
          </tbody>
        </table>
        
      </div>
    </div>
  );
}