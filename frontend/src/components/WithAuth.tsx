"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import axios, { AxiosError } from "axios";
import { useToast } from "@/components/ui/use-toast";

export const withAuth = (Component:any) => {
  const AuthenticatedComponent = () => {
    const router = useRouter();
    const [data, setData] = useState({ isLoggedIn: false});
    const { toast } = useToast();

    useEffect(() => {
      const verifyToken = async () => {
        // Check local storage for access token
        const accessToken = localStorage.getItem("accessToken");

        // If access token is not found, redirect to login
        if (!accessToken) {
          router.push("/auth/login");
          return;
        }

        try {
          const response = await axios.post(
            `${process.env.NEXT_PUBLIC_BACKEND_DOMAIN}/api/user/token/verify/`,
            {
              token: accessToken,
            }
          );
        } catch (error:any) {
          // Handle login errors
          if (error.response) {
            // Server responded with an error
            toast({
              title: "Login unsuccessful",
              description:
                error.response.data.detail || "An error occurred during login.",
            });
          } else if (error.request) {
            // The request was made but no response was received
            toast({
              title: "Network error",
              description: "Please check your internet connection.",
            });
          } else {
            // Something happened in setting up the request that triggered an error
            toast({
              title: "Unexpected error",
              description:
                "An unexpected error occurred. Please try again later.",
            });
          }

          router.push("/auth/login");

          return;
        }

        setData({ isLoggedIn: true });
      };
      verifyToken();
    }, []);

    return !!data ? <Component data={data} /> : null; // Render whatever you want while the authentication occurs
  };

  return AuthenticatedComponent;
};
