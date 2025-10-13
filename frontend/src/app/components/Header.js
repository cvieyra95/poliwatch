import Image from "next/image"
import logo from "../../assets/Logo.png"
import style from "./Header.module.css"
import Link from "next/link";
export default function Header(){
    return (
        <div className={style.header}>
            <Image src={logo} alt="poliwatch logo" className={style.logo}/>
            <button className={style.donation}><Link href="/donate">Donate</Link></button>
        </div>
    )
}