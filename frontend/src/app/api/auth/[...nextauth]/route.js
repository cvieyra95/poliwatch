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
                const response = await fetch("https://authforpoliwatch-production.up.railway.app/auth/token", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                    email: credentials.email,
                    password: credentials.password
                })
            })

            const data = await response.json();
            console.log("USER FROM BACKEND:", data);


            if(response.ok && data.user){
                return{
                    id: data.user.id,
                    email: data.user.email,
                    firstName: data.user.first_name,
                    lastName: data.user.last_name,
                    //zipcode: data.user.zipcode
                }
            }
            else{
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
                token.firstName = user.firstName,
                {/*token.zipcode = user.zipcode */}
            }

            return token
        },
    async session({session, token}){
        if(token)
        {
            session.user.firstName = token.firstName,
            {/* session.user.zipcode = token.zipcode */}
        }
        console.log("update after ", token)
        return session
        }
    }
})

export {handler as GET, handler as POST}