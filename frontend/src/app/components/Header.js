'use client'
import Image from "next/image"
import logo from "../../assets/Logo.png"
import style from "./Header.module.css"
import Link from "next/link";
import { useRouter } from 'next/navigation'
export default function Header(){

    const router = useRouter()
    const donateButton = () => {
        router.push('/donate')
    }
    return (
        <div className={style.header}>
            <Image src={logo} alt="poliwatch logo" className={style.logo}/>
            <button onClick={donateButton} className={style.donation}>Donate</button>
        </div>
    )
}