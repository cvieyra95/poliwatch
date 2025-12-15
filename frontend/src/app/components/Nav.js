'use client'
import Link from "next/link";
import { signOut, useSession } from "next-auth/react"

export default function Nav() {
    const {data: session} = useSession()
    console.log(session)

    return(
        <nav>
            <div className="nav-left">
                <Link href="/">Home</Link>
                <Link href="/politicians">Politicians</Link>
                <Link href="/contact">Contact</Link>
            </div>
           
            
             {session ? (
                <div className="greeting"> 
                <h3>Welcome, {session.user.username}</h3>

                {/*Functional Requirement 9: allow users to log out from the Poliwatch Hub */}
                <button onClick={() =>signOut({callbackUrl:process.env.NEXTAUTH_URL})}>Sign Out</button>
                </div>
                ) : (
                     <div className="nav-right">
                     <Link href="/signin">Sign In</Link>   
                    </div>
                )}
        </nav>
    )
}