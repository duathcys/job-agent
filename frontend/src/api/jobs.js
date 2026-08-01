import client from './client';

export const getRecommendations = () => client.get('/agent/recommendations');
export const runAgent = () => client.post('/agent/run');
export const getJobs = () => client.get('/jobs/');