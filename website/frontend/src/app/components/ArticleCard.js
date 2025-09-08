// components/ArticleCard.js
import styles from "./ArticleCard.module.css"

export default function ArticleCard({ article }) {
  return (
    <article className={styles.article}>
      <img src={article.thumbnail ?? "/Images/default.jpg"} alt={article.title} />
      <div className={styles.text}>
        <h3>
          <a href={article.link}>{article.title}</a>
        </h3>
        <p>{article.snippet}</p>
      </div>
    </article>
  );
}
