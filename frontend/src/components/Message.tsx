import { CodeMessage, parseCode } from "@/mylib/utils";
import { Logo } from "./assets/Icons";
import { Avatar, AvatarImage } from "./ui/avatar";
import { useState, useEffect } from "react";
import Typewriter from "typewriter-effect";
import Code from "./Code";

type File = {
  name: string;
  type: string;
  data?: string;
};

type MessageProps = {
  message: string;
  id: string;
  isUser: boolean;
  isNew?: boolean;
  file?: File; // Include the file prop
};

export default function Message({
  id,
  isUser,
  message,
  isNew = false,
  file=undefined, // Destructure the file prop
}: MessageProps) {
  const { codesArr, withoutCodeArr } = parseCode(message);
  let result = withoutCodeArr.map((item, index) => {
    return codesArr[index] ? [item, codesArr[index]] : [item];
  });

  return (
    <div
      className={`${!isUser ? "py-7" : "py-1"} h-fit ${
        !isUser ? "dark:bg-neutral-900 bg-neutral-100" : "bg-inherit"
      }`}
    >
      <div className="flex flex-row gap-6 w-[40%] max-[900px]:w-[88%]  mx-auto items-start">
        {isUser ? (
          <>
            <Avatar className="w-10 h-10">
              <AvatarImage src="https://ui.shadcn.com/avatars/01.png" />
            </Avatar>
          </>
        ) : (
          <span className="">{Logo}</span>
        )}
        <span className="leading-8 w-[97%]">
          {isUser || !isNew ? (
            <>
              {result.flat().map((item: any, index: number) => {
                return (
                  <div key={id + index}>
                    {typeof item == "string" ? (
                      item
                    ) : (
                      <div className="mb-1 w-[94%] z-50">
                        <Code language={item.language}>{item.code}</Code>
                      </div>
                    )}
                  </div>
                );
              })}
            </>
          ) : (
            <>
              {result.flat().map((item: any) => {
                return (
                  <>
                    {typeof item == "string" ? (
                      <TypeOnce>{item}</TypeOnce>
                    ) : (
                      <div className="mb-1 w-[94%] z-50">
                        <Code language={item.language}>{item.code}</Code>
                      </div>
                    )}
                  </>
                );
              })}
            </>
          )}

          {/* Render file content if it exists */}
          {file && (
            <div className="flex items-center gap-2">
              <span className="font-semibold">File:</span>
              <span>{file.name}</span>
              <span>({file.type})</span>
            </div>
          )}
        </span>
      </div>
    </div>
  );
}

export function Skeleton() {
  return (
    <div className={`py-7 h-fit dark:bg-neutral-900 bg-neutral-100`}>
      <div className="flex flex-row gap-6 w-[40%] max-[900px]:w-[88%]  mx-auto items-start">
        <span className="">{Logo}</span>
        <span className="leading-8">
          <Typewriter
            options={{
              delay: 5,
              loop: true,
              autoStart: true,
            }}
            onInit={(typewriter) => {
              typewriter.typeString("...").start();
            }}
          />
        </span>
      </div>
    </div>
  );
}

function TypeOnce({ children }: { children: string }) {
  const [on, setOn] = useState(true);
  return on ? (
    <Typewriter
      options={{
        delay: 45,
      }}
      onInit={(typewriter) => {
        typewriter
          .typeString(children)
          .start()
          .callFunction(() => {
            setOn(false);
          });
      }}
    />
  ) : (
    children
  );
}
