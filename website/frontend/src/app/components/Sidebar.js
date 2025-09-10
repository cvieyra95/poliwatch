// components/Sidebar.js
import styles from "./Sidebar.module.css"
export default function Sidebar() {
  return (
    <div className={styles.sidebar}>
      <div className={styles.tradebox}>
        <div className={styles.tradeheader}>
          <h3>Latest Trades</h3>
          <a className={styles.viewall}>Vew All</a>
        </div>
        <ul className={styles.trades}>
          <li>
            <strong>Nancy Pelocy</strong> BUY  ACTION
            <br/>
            <small>09/1/2025 | Democrat</small>
          </li>
        </ul>
        
      </div>
    </div>
  );
}
