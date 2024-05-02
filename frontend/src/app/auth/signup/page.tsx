"use client";

import { Logo } from "@/components/assets/Icons";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import Link from "next/link";
import { useState } from "react";
import { useToast } from "@/components/ui/use-toast";
import { useRouter } from "next/navigation";
import axios, { AxiosError } from "axios";

export default function Signup() {
  const [inputs, setInputs] = useState({
    email: "",
    username: "",
    password: "",
  });
  const { toast } = useToast();
  const { push } = useRouter();

  function handleSignup() {
    const { email, username, password } = inputs;
    axios
      .post(`${process.env.NEXT_PUBLIC_BACKEND_DOMAIN}/api/user/signup/`, {
        email,
        username,
        password,
      })
      .then(({ data }) => {
        localStorage.setItem("user", JSON.stringify(data));
        push("/auth/login");
      })
      .catch((err) => {
        if (err instanceof AxiosError)
          toast({
            title: "Signup unsuccessful",
            description: JSON.stringify(err.response?.data),
          });
      });
  }

  return (
    <div className="flex flex-col items-center h-screen">
      <span className="mt-12">{Logo}</span>
      <Card className="w-[380px] py-5 mt-20 max-[900px]:mt-10 max-[400px]:w-[95%]">
        <CardHeader>
          <CardTitle>New to ChatGPT</CardTitle>
          <CardDescription>Create your account.</CardDescription>
        </CardHeader>
        <CardContent>
          <form>
            <div className="grid w-full items-center gap-4 mt-1">
              <div className="flex flex-col gap-3  space-y-1.5">
                <Label htmlFor="email">Email </Label>
                <Input
                  value={inputs.email}
                  onChange={(e) =>
                    setInputs((prev) => ({ ...prev, email: e.target.value }))
                  }
                  id="email"
                  placeholder="john.doe@example.com"
                />
              </div>
              <div className="flex flex-col gap-3  space-y-1.5">
                <Label htmlFor="username">Username</Label>
                <Input
                  value={inputs.username}
                  onChange={(e) =>
                    setInputs((prev) => ({ ...prev, username: e.target.value }))
                  }
                  id="username"
                  placeholder="johndoe"
                />
              </div>
              <div className="flex flex-col gap-3 mt-2 space-y-1.5">
                <Label htmlFor="password">Password</Label>
                <Input
                  value={inputs.password}
                  onChange={(e) =>
                    setInputs((prev) => ({ ...prev, password: e.target.value }))
                  }
                  type="password"
                  id="password"
                />
              </div>
            </div>
          </form>
        </CardContent>
        <CardFooter className="flex mt-1">
          <Button
            disabled={!inputs.email || !inputs.password || !inputs.username}
            onClick={handleSignup}
            variant="custom"
            className="w-full"
          >
            Signup
          </Button>
        </CardFooter>
      </Card>
      <span className="mt-6 text-sm max-[400px]:pb-4">
        Already have an account?{" "}
        <Link className="text-neutral-400" href="/auth/login">
          Log in
        </Link>{" "}
      </span>
    </div>
  );
}
