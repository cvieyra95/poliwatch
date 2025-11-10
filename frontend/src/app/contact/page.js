import Header from "../components/Header"
import Nav from "../components/Nav"
import Footer from "../components/Footer"
import styles from "./contact.module.css"

export default function Contact() {


    return(
        <div>
            <Header/>
            <Nav/>
            <div className={styles.container}>
                <div className={styles.title}>
                    <h1>Contact Us</h1>
                </div>
                <div className={styles.form}>
                    <h2>Get In Touch</h2>
                        <div className={styles.row}>
                            <input type="text" value="Name"></input>
                            <input type="text" value="Email"></input>
                        
                        </div>
                        <textarea className={styles.message} name="message" rows="40" cols="30" value="Message"></textarea>
                        <br></br>
                        <input type="button" value="Submit"></input>
                        
                </div>
            </div>
            <Footer/>
        </div>
    )
}