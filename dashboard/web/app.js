const e = React.createElement;

// When index.html is opened directly from the filesystem (file://),
// fetch requests need an explicit server origin. Default to the
// local dashboard API if no origin is present.
const API_BASE = window.location.protocol === 'file:' ? 'http://127.0.0.1:8000' : '';

function useFetch(url) {
  const [data, setData] = React.useState(null);
  React.useEffect(() => {
    const fetchData = () => fetch(url).then(r => r.json()).then(setData).catch(() => {});
    fetchData();
    const id = setInterval(fetchData, 2000);
    return () => clearInterval(id);
  }, [url]);
  return data;
}

function Dashboard() {
  const status = useFetch(API_BASE + '/status');
  const messages = useFetch(API_BASE + '/messages');
  return e('div', null,
    e('h2', null, 'Agents'),
    e('pre', null, JSON.stringify(status, null, 2)),
    e('h2', null, 'Messages'),
    e('pre', null, JSON.stringify(messages, null, 2))
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(e(Dashboard));
