//Functional Requirement #3
'use client'
import { use, useState } from "react"
import Header from "../components/Header"
import Nav from "../components/Nav"
import styles from "./signup.module.css"
import Footer from "../components/Footer"

export default function Signup(){

    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")
    const [firstName, setFirstName] = useState("")
    const [lastName, setLastName] = useState("")
    const [zipCode, setZipCode] = useState("")

    const handleSubmit = async () => {
        if(password !== confirmPassword)
        {
            alert("password does not match")
            return
        }
        const response = await fetch("https://authforpoliwatch-production.up.railway.app/auth/", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                email, 
                first_name: firstName, 
                last_name: lastName, 
                //zipcode: zipCode, 
                password,
                confirm_password: confirmPassword
            })
        })

        const data = await response.json()

        if(response.ok)
        {
            router.push("/signin")
        }
        else{
            alert("Something went wrong try again. ")
        }
    }

    return(
        <div>
            <Header/>
            <Nav/>

            <div className={styles.signup}>
                <h2>Create An Account</h2>
                <div className={styles.form}>
                <input type="text" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email"></input>
                <input type="text" value={firstName} onChange={(e) => setFirstName(e.target.value)} placeholder="First Name"></input>
                <input type="text" value={lastName} onChange={(e) => setLastName(e.target.value)} placeholder="Last Name"></input>
                {/*<input type="text" value={zipCode} onChange={(e) => setZipCode(e.target.value)} placeholder="Zip code"></input> */}

                <input type="password" value={password}onChange={(e) => setPassword(e.target.value)}placeholder="Password"></input>
                <input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)}placeholder="Confirm Password"></input>
                </div>

                <button onClick={handleSubmit} className= {styles.signupbutton} type="button">Sign Up</button>
                </div>
                <div className={styles.footer}>
                    <Footer/>
                </div>
                
        </div>
    )
}


/*{
    "username": "johndoe",
    "password": "supersecret",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
}
    */