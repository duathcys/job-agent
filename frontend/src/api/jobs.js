import client from './client';

export const getRecommendations = () => client.get('/agent/recommendations');
export const getJobs = () => client.get('/jobs/');

export const runAgentStream = (onMessage, onDone, onError) => {
  const token = localStorage.getItem('token');
  const url = `${import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'}/agent/run-stream`;

  const eventSource = new EventSource(`${url}?token=${token}`);

  eventSource.onmessage = (e) => {
    const data = JSON.parse(e.data);
    if (data.done) {
      onDone();
      eventSource.close();
    } else if (data.error) {
      onError(data.error);
      eventSource.close();
    } else {
      onMessage(data.message);
    }
  };

  eventSource.onerror = () => {
    onError('연결 오류가 발생했습니다.');
    eventSource.close();
  };

  return eventSource;
};