
import Header from "./components/Header"
import Nav from "./components/Nav"
import ArticleCard from "./components/ArticleCard"
import Sidebar from "./components/Sidebar"
import Bills from "./components/Bills"
import Footer from "./components/Footer"


const API_KEY = process.env.NEWS_API_KEY;

async function fetchArticles() {

  
  let q = 'politics'
  let sources = 'politico, cnn'
  let language = 'en'
  const url = new URL(`https://newsapi.org/v2/everything?q=${q}&sources=${sources}&language=${language}&apiKey=${API_KEY}`);//Calls News API, we can change this

  const response = await fetch(url, {next: { revalidate: 3600 }});
  const data = await response.json()
  return (
    data.articles.map((a) => ({
      title: a.title,
      link: a.url,
      snippet: a.description,
      source: a.source.name,
      thumbnail: a.urlToImage || "/Images/default.jpg",
    } || []))
  );
}

export default async function Home() {
  const articles = await fetchArticles()
  return (
    <div>
      <Header />
        <Nav />
          <main className="main">
            {articles[0] && (
              <section className="mainarticle">
                <img src={articles[0].thumbnail} alt={articles[0].title}/>
                <div className="description">
                  <h2>
                    <a href={articles[0].link} target="_blank">{articles[0].title}</a>
                  </h2>
                  <p>{articles[0].snippet}</p>
                  <span className="source">Source: {articles[0].source}</span>
                </div>
              </section>
            )}

            <section className="otherarticles">
              {articles.slice(1,4).map((a,i) =>(
                <ArticleCard key={i} article = {a} />
              ))}
            </section>
            <Sidebar/>
            <Bills/>
          </main>
          <Footer/>
    </div>
  );
}