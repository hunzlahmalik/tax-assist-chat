import axios from "axios";

const axiosInstance = axios.create({});

// set base domain for axios instance
axiosInstance.defaults.baseURL = process.env.NEXT_PUBLIC_BACKEND_DOMAIN || "";

// add authorization if accessToken found in localStorage
axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem("accessToken");
  if (token) {
    config.headers["Authorization"] = `Bearer ${token}`;
  }
  return config;
});

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (
      error.response.status === 401 &&
      error.response.data.code === "token_not_valid"
    ) {
      try {
        await axiosInstance.post(`api/user/token/refresh`);
        return await axiosInstance(originalRequest);
      } catch (err) {
        console.log(err);
      }
    }

    return Promise.reject(error);
  }
);

export const httpRequest = axiosInstance;
