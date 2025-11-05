import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials"

const handler = NextAuth({

    providers: [
        CredentialsProvider({
            name: "Credentials",
            credentials : {
                email: { label: "emaile", type: "email", placeholder: "email" },
                password: { label: "Password", type: "password" }
            },
            async authorize(credentials, req){
                try {
                    const response = await fetch("https://authforpoliwatch-production.up.railway.app/auth/token", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                        email: credentials.email,
                        password: credentials.password
                    })
            })
            if (!response.ok){
                console.error("Backend Auth Failed", await response.text())
            }

            const data = await response.json();
            console.log("USER FROM BACKEND:", data);


            if(data && data.user){
                return{
                    id: data.user.id,
                    email: data.user.email,
                    firstName: data.user.first_name,
                    lastName: data.user.last_name
                }
            }
            return null
        } catch(err){
            console.error("Authorize error:", err)
            return null
        }
        }
    })
    ],
    session:{
        strategy: "jwt"
    },
    pages: {
        signIn: "/signin"
    },
    callbacks: {
        async jwt({token, user}){
            if(user)
            {
                console.log("adding token", user)
                token.firstName = user.firstName
            }

            return token
        },
    async session({session, token}){
        if(token)
        {
            session.user.firstName = token.firstName
        }
        console.log("update after ", token)
        return session
        }
    }
})

export {handler as GET, handler as POST}