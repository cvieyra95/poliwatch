import Header from "../components/Header"
import Nav from "../components/Nav"
import styles from "./about.module.css"
import Footer from "../components/Footer"


export default function About() {


    return(
        <div>
            <Header/>
            <Nav/>
            <div className={styles.header}>
                <h1>About PoliWatch</h1>
            </div>
            <div className={styles.about}>
                <p>This is our project for CPSC 491 </p>
            </div>
            <Footer/>
        </div>
    )
}