"use client"
import styles from "./trades.module.css"
import { useState, useEffect } from "react";
import Header from "../components/Header"
import Nav from "../components/Nav"
import Footer from "../components/Footer"


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
        <Header/>
        <Nav/>
      <div className={styles.tradebox}>
        <div className={styles.tradeheader}>
          <h3>All Latest Stock Trades</h3>
        </div>
         <table className={styles.table}>
          <thead>
            <tr>
              <th>Name</th>
              <th>Symbol</th>
              <th>Type</th>
              <th>Amount</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {trades.map((p, index) => {
              const tradeType = p.type.toLowerCase() === "buy" ? styles.buy : styles.sell
              return (
                
                <tr className={styles.row} key={`${p.name}-${p.company}-${index}`}>
                  <td>{p.name}</td>
                  <td className={styles.symbol}><a href={`https://www.google.com/search?q=${p.company}`} target="_blank">${p.company}</a></td>
                  <td className={`${styles.type} ${tradeType}`}>{p.type.toUpperCase()}</td>
                  <td className={`${styles.type}`}>{p.amount}</td>
                  <td>{new Date(p.date).toLocaleDateString()}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
        
      </div>
      <Footer/>
    </div>
  );
}