import Header from "../../components/Header"
import Nav from "../../components/Nav"
import styles from "./profile.module.css"
import Footer from "../../components/Footer"
import Image from "next/image"
import twitter from "../../logos/twitter.png"
import instagram from "../../logos/instagram.png"
import facebook from "../../logos/facebook.png"



export default async function profile({params}) {
    const {id} = await params

    const response =  await fetch(`https://apibackend-production-e816.up.railway.app/members/${id}`); 
    const data = await response.json()

    const resp = await fetch (`https://apibackend-production-e816.up.railway.app/bio/${id}`)
    const bio = await resp.json()

    const social =  await fetch (`https://apibackend-production-e816.up.railway.app/socials/by-member/${data.id}`)
    const socials = await social.json()

    /*
    const vote_records = await fetch(`https://apibackend-production-e816.up.railway.app/vote_records/by-member/${data.id}`)
    const vote_records_data_raw = await vote_records.json()
    const vote_records_data = Array.isArray(vote_records_data_raw) ? vote_records_data_raw : vote_records_data_raw.data || [];

    const bills = await Promise.all(
        vote_records_data.map(async (record) => {
            const response = await fetch(`https://apibackend-production-e816.up.railway.app/vote/${record.vote_id}`);
            const billData = await response.json();
            return {
                ...billData,
                vote_id: record.vote_id,
                position: record.position
            }
        })
    )   

    const orderedBills = bills.sort((a, b) => new Date(b.date) - new Date(a.date));
    */

    return(
        <div>
            <Header/>
            <Nav/>
            <div className={styles.container}>
                <div className={styles.intro}>
                    <img src={data.image_url} alt="portrait" height="250" width="200"/>
                    <h1 className={styles.name}>{data.first_name} {data.last_name}</h1>
                </div>
                <div className={styles.bio}>
                    <h2>Biography</h2>
                    <p>{bio.summary}</p>
                    <div className={styles.website}>
                        <h2>Websites</h2>
                        <a href={`https://www.congress.gov/member/${data.first_name.toLowerCase()}-${data.last_name.toLowerCase()}/${id}`} target="_blank">Congress Website</a>
                        <a href={socials.official_website} target="_blank">Official Website</a>
                    </div>

                    <div className={styles.finance}>
                        <h2>Financial Data</h2>
                        <a href={`https://www.opensecrets.org/members-of-congress/summary?cid=${socials.opensecrets_id}`} target="_blank">opensecrets.org</a>
                    </div>
                    <div className={styles.socials}>
                    <h2>Social Media Links</h2>
                    <a href={`https://twitter.com/${socials.twitter_handle}`} alt="twitter" target="_blank">
                    <Image src={twitter} alt="twitter" width="60" height="60"/>
                    </a>
                    <a href={`https://instagram.com/${socials.instagram}`} alt="instagram" target="_blank">
                    <Image src={instagram} alt="instagram" width="60" height="60"/>
                    </a>
                    <a href={`https://facebook.com/${socials.facebook}`} alt="facebook" target="_blank">
                    <Image src={facebook} alt="facebook" width="60" height="60"/>
                    </a>

                </div>
                </div>
            </div>
            <Footer/>
        </div>
    )
}