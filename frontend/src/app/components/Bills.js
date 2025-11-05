
"use client";
import styles from "./Bills.module.css"
import { useState, useEffect } from "react";

export default function Bills() {

  const [bills, setBills] = useState([])
  const [votes, setVotes] = useState([])
  useEffect(() => {
      async function fetchBills() {
        try {
          const res = await fetch("https://apibackend-production-e816.up.railway.app/bills/?congress=119&limit=15") //Call API for Bills
          const data = await res.json()
          setBills(data);
        } catch (err) {
          console.error("Error fetching Bills:", err)
        }
      }
      fetchBills();
    }, []);

  return (
    <div className={styles.sidebar}>
      <div className={styles.billbox}>
        <div className={styles.billheader}>
          <h3>Latest Bills</h3>
          <a className={styles.viewall}>Vew All</a>
        </div>
         <table className={styles.table}>
          <thead>
            <tr>
              <th>Chamber</th>
              <th>Bill</th>
              <th>Date Introduced</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {bills.map((b) => {
              return (
              <tr key={b.id}>
                <td>{b.congress}</td>
                <td><a href={`https://www.congress.gov/bill/119th-congress/${b.bill_type}/${b.bill_number}`} target="_blank"> {b.bill_type} {b.number}</a></td>
                <td>{b.introduced_date}</td>
                <td>{}</td>
                </tr>

           )})}
          </tbody>
        </table>
        
      </div>
    </div>
  );
}
