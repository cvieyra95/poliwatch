//Functional Requrement #6
"use client"; // needed for useState & useEffect
import Header from "../components/Header"
import Nav from "../components/Nav"
import { useState, useEffect } from "react";
import styles from "./politicians.module.css";
import Footer from "../components/Footer"
import { useRouter } from "next/navigation";

export default function Politicians() {
  const [politicians, setPoliticians] = useState([]);
  const [sortBy, setSortBy] = useState("name"); //Default sort is by name
  const router = useRouter();

  useEffect(() => {
    async function fetchData() {
      const limit = 200
      let offset = 0
      let allMembers = []
      let keepFetching = true
      try {
        while (keepFetching) {
          const response = await fetch(
            `https://apibackend-production-e816.up.railway.app/members?chamber=house&limit=${limit}&offset=${offset}`
          );
          const data = await response.json();

          if (!Array.isArray(data) || data.length === 0) {
            keepFetching = false;
            break;
          }

          allMembers = [...allMembers, ...data];
          offset += limit;
        }

        setPoliticians(allMembers);
      } catch (err) {
        console.error("Error fetching politicians:", err);
      }
    }

    fetchData();
  }, []);

  const sortedPoliticians = [...politicians].sort((a, b) => {
    if (sortBy === "name") return a.last_name.localeCompare(b.last_name);
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
        <h2>Members of Congress</h2>
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
                <tr className={styles.row} key={p.bioguide_id} onClick={() => router.push(`/politicians/${p.bioguide_id}`)}>
                  <td>{p.district}</td>
                  <td>{p.last_name} {p.first_name}</td>
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
          <tr className={styles.row} key={p.bioguide_id} onClick={() => router.push(`/politicians/${p.bioguide_id}`)}>
            <td>{p.last_name} {p.first_name}</td>
            <td>{p.state}</td>
            <td>{p.party}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )}
    </div>
    <Footer/>
    </div>
  );
}
