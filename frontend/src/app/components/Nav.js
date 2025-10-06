import Link from "next/link";

export default function Nav() {
    return(
        <nav>
            <div className="nav-left">
                <Link href="/">News</Link>
                <Link href="/politicians">Politicians</Link>
                <Link href="/activists">Activists</Link>
            </div>
            <div className="nav-right">
                <Link href="/signin">Sign In</Link>
            </div>
            
        </nav>
    )
}