
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
    const billType = {
      hr: "hr",
      s: "s",
      hconres: "house-concurrent-resolution",
      sconres: "senate-concurrent-resolution",
      hjres: "house-joint-resolution",
      sjres: "senate-joint-resolution"
    }
    function truncateWords(text, maxWords){
      const words = text.split(" ")
        if(words.length > maxWords)
        {
          return words.slice(0, maxWords).join(" ") + "..."
        }
        return text


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
              <th>Title</th>
            </tr>
          </thead>
          <tbody>
            {bills.map((b) => {
                const type = billType[b.bill_type.toLowerCase()]
                const shortTitle = truncateWords(b.title, 8)
              return (
              <tr key={b.id}>
                <td>{b.congress}</td>
                <td><a href={`https://www.congress.gov/bill/${b.congress}-congress/${type}}/${b.number}`} target="_blank"> {b.bill_type.toUpperCase()} {b.number}</a></td>
                <td>{new Date(b.introduced_date).toLocaleDateString()}</td>
                <td>{shortTitle}</td>
                </tr>

           )})}
          </tbody>
        </table>
        
      </div>
    </div>
  );
}
