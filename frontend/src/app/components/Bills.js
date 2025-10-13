
"use client";
import styles from "./Bills.module.css"
import { useState, useEffect } from "react";

export default function Bills() {

  const [bills, setBills] = useState([]);
  useEffect(() => {
      async function fetchBills() {
        try {
          const res = await fetch("http://127.0.0.1:8000/bills"); //Call API for Bills
          const data = await res.json();
          setBills(data);
        } catch (err) {
          console.error("Error fetching Bills:", err);
        }
      }
      fetchBills();
    }, []);

    function getStatus(latestAction){

      if (!latestAction) return "Unknown";

      const text =  latestAction.toLowerCase();
      
      if(text.includes("passed") || text.includes("became public law")){
        return("Passed");
      }
      if(text.includes("vote") || text.includes("calendar") || text.includes("introduced")){
        return("Pending Vode");
      }
      return "Introduced";
    }

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
                <td>{b.origin_chamber}</td>
                <td><a href={`https://www.congress.gov/bill/119th-congress/${b.bill_type}/${b.bill_number}`} target="_blank"> {b.bill_type} {b.bill_number}</a></td>
                <td>{b.update_data}</td>
                <td>{getStatus(b.action)}</td>
                </tr>

           )})}
          </tbody>
        </table>
        
      </div>
    </div>
  );
}
