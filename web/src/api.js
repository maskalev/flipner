import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'http://test.msklv.ru:8000/api/v1/',
    headers: {
        'Content-Type': 'application/json',
    },
});

export default apiClient;
