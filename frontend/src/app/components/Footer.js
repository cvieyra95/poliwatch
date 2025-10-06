import Image from "next/image"
import style from "./Footer.module.css"
import Link from "next/link";
import logo from "../../assets/Logo.png"

export default function Footer(){
    return (
        <div className={style.header}>
            <div className={style.spacer}></div>
            <div className={style.logo}>
                <Image src={logo} alt="poliwatch logo" className={style.logo}/>
            </div>
            <div className={style.nav}>
                <Link href="/">Home</Link>
                <Link href="/about">About</Link>
                <Link href="/contact">Contact Us</Link>
                <Link href="/donate">Donate</Link>
            </div>

        </div>
    )
}