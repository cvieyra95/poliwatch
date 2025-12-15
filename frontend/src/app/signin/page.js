'use client'
import Header from "../components/Header"
import Nav from "../components/Nav"
import styles from "./signin.module.css"
import Footer from "../components/Footer"
import Link from "next/link"

import { useRouter } from 'next/navigation'
import { signIn } from "next-auth/react"
import { useState } from "react"


export default function Signin() {

    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")

    const router = useRouter()

    const handleSignIn = async () => {
        const response = await signIn("credentials", {
            username, 
            password, 
            redirect: false
        })
        if(response.ok)
        {
            router.push("/")
        }
        else{
            alert("Failed to login")
        }
    }
    //Functional Requirement #8
    //Logging into Poliwatch Hub 

    return(
        <div>
            <Header/>
            <Nav/>
            <div className={styles.signin}>
                <h1>Sign In</h1>
                <div className={styles.form}>
                <input type="username"  value={username} name= "username" onChange={(e) => setUsername(e.target.value)} placeholder="Username"></input>
                <input type="password" value={password} name="password" onChange={(e) => setPassword(e.target.value)} placeholder="Password"></input>
                </div>
                <div className={styles.rememberme}>
                <input type="checkbox"/>
                <label>Remember Me</label>
                </div>
                <button className= {styles.signIn} onClick={handleSignIn} type="submit">Sign In</button>
                </div>

                <div className={styles.signUp}>
                    <p>New User? </p>
                    <p className={styles.link}><Link href="/signup">Sign Up</Link></p>
            </div>
            <div className={styles.footer}>
            <Footer/>
            </div>
            
        </div>
        
    )
}