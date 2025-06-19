const e = React.createElement;

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
  const status = useFetch('/status');
  const messages = useFetch('/messages');
  return e('div', null,
    e('h2', null, 'Agents'),
    e('pre', null, JSON.stringify(status, null, 2)),
    e('h2', null, 'Messages'),
    e('pre', null, JSON.stringify(messages, null, 2))
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(e(Dashboard));
