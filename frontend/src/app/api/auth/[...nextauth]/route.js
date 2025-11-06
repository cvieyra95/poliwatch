import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials"

const handler = NextAuth({
    providers: [
        CredentialsProvider({
            name: "Credentials",
            credentials : {
                username: { label: "username", type: "username", placeholder: "username" },
                password: { label: "Password", type: "password" }
            },
           async authorize(credentials) {
  try {
    // Send form-encoded data (what FastAPI expects)
    const response = await fetch(
      "https://authforpoliwatch-production.up.railway.app/auth/token",
      {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          username: credentials.username,
          password: credentials.password,
        }),
      }
    );

    if (!response.ok) {
      console.error("Backend auth failed:", await response.text());
      return null;
    }

    const data = await response.json();
    console.log("USER FROM BACKEND:", data);

    if (data.access_token) {
      return {
        id: credentials.username,   
        username: credentials.username,
        accessToken: data.access_token,
      };
    }

    return null;
  } catch (err) {
    console.error("Authorize error:", err);
    return null;
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