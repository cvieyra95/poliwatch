'use client'
import Header from "../components/Header"
import Nav from "../components/Nav"
import Footer from "../components/Footer"
import styles from "./donate.module.css"
import React, {useState} from "react"

export default function Donate() {
    const [customAmount, setCustomAmount] = useState('')
    const handleChange = (event) => {
        setCustomAmount(event.target.value)
    }

    return(
        <div>
            <Header/>
            <Nav/>
            
            <div className={styles.title}>
                <h1>Donate</h1>
            </div>
            <div className={styles.container}>
            <div className={styles.donate}>
                <h2>Select An Amount</h2>
            <div className={styles.amount}>
                
                <input type="button" value="$1"></input>
                <input type="button"  value="$10"></input>
                <input type="button"  value="$20"></input>
                <input type="button" value="$50"></input>
            </div>
                <div className={styles.custom}>
                <input type="number" value={customAmount} onChange={handleChange} placeholder="$Custom Amount"></input>
                </div>
                <div className={styles.submit}>
                <input type="button" value="Submit"></input>
                </div>            
            
            </div>
            </div>

            <Footer/>
        </div>
    )
}