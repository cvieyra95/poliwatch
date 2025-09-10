
import Header from "./components/Header"
import Nav from "./components/Nav"
import ArticleCard from "./components/ArticleCard"
import Sidebar from "./components/Sidebar"

const API_KEY = process.env.NEWS_API_KEY;

async function fetchArticles() {
  const url = new URL("https://newsapi.org/v2/everything");
  url.searchParams.set("q", "politics OR election OR government");
  url.searchParams.set("language", "en");
  url.searchParams.set("sortBy", "publishedAt");
  url.searchParams.set("apiKey", API_KEY);

  const res = await fetch(url.toString(), {
    next: { revalidate: 3600 }, // revalidate every hour
  });

  console.log(res)
  const data = await res.json();

  return (
    data.articles?.map((a) => ({
      title: a.title,
      link: a.url,
      snippet: a.description,
      source: a.source.name,
      thumbnail: a.urlToImage || "/Images/default.jpg",
    })) || []
  );
}



export default async function Home() {
  const articles = await fetchArticles()
  return (
    <div>
      <Header />
        <Nav />
          <main className="main">
            {/* Main Article */}
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
          </main>
    </div>
  );
}