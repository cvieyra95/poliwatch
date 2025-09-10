"use client"; // needed for useState & useEffect

import Header from "../components/Header"
import Nav from "../components/Nav"
import { useState, useEffect } from "react";
import styles from "./politicians.module.css";

export default function Politicians() {
  const [politicians, setPoliticians] = useState([]);
  const [sortBy, setSortBy] = useState("name"); //Default sort is by name

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch("http://localhost:3001/politicians"); //API
        const data = await res.json();
        setPoliticians(data);
      } catch (err) {
        console.error("Error fetching politicians:", err);
      }
    }
    fetchData();
  }, []);

  const sortedPoliticians = [...politicians].sort((a, b) => {
    if (sortBy === "name") return a.name.localeCompare(b.name);
    if (sortBy === "state") return a.state.localeCompare(b.state);
    return 0;
  });
  const groupedByState = sortedPoliticians.reduce((acc, p) => {
  if (!acc[p.state]) acc[p.state] = [];
  acc[p.state].push(p);
  return acc;
  }, {});

  return (
    <div> 
        <Header/>
        <Nav/>
    <div className={styles.container}>
        <h2>Memebers of Congress</h2>
      <div className={styles.sortControls}>
        <button value="name" onClick={(e) => setSortBy(e.target.value)}>By Last Name</button>
        <button value="state" onClick={(e) => setSortBy(e.target.value)}>By State</button>
      </div>

      {sortBy === "state" ? (
    Object.keys(groupedByState).map((state) => (
      <div key={state} className={styles.stateGroup}>
        <h4 className={styles.stateHeader}>{state.toUpperCase()}</h4>
        <table className={styles.table}>
          <thead>
            <tr>
              <th>District</th>
              <th>Name</th>
              <th>State</th>
              <th>Party</th>
            </tr>
          </thead>
          <tbody>
            {groupedByState[state]
              .sort((a, b) => a.district - b.district)
              .map((p) => (
                <tr className="row" key={p.id} onClick={() => window.open(p.url, "_blank")}>
                  <td>{p.district}</td>
                  <td>{p.name}</td>
                  <td>{p.state}</td>
                  <td>{p.party}</td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>
    ))
  ) : (
    <table className={styles.table}>
      <thead>
        <tr>
          <th>Name</th>
          <th>State</th>
          <th>Party</th>
        </tr>
      </thead>
      <tbody>
        {sortedPoliticians.map((p) => (
          <tr className="row" key={p.id} onClick={() => window.open(p.url, "_blank")}>
            <td>{p.name}</td>
            <td>{p.state}</td>
            <td>{p.party}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )}
    </div>
    </div>
  );
}
