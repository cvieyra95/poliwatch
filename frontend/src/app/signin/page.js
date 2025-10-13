import Header from "../components/Header"
import Nav from "../components/Nav"
import styles from "./signin.module.css"

export default function Signin() {


    return(
        <div>
            <Header/>
            <Nav/>

            <div className={styles.signin}>
                <h1>Sign In</h1>
                <div className={styles.form}>
                <input type="text" placeholder="Email"></input>
                <input type="password" placeholder="Password"></input>
                </div>
                <div className={styles.rememberme}>
                <input type="checkbox"/>
                <label>Remember Me</label>
                </div>
                <button type="button">Sign In</button>
            </div>
        </div>
    )
}