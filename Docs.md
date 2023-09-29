## Initialize the Project

1. npx create-next-app@latest --typescript --tailwind --eslint
2. npx shadcn-ui@latest init
3. clean the project structure like page.tsx file.
4. setup the shadcn ui library.
5. add the button component from the shadcn ui.
6. There is function named cn in lib/utils folder, the use of this function is to make tailwind css dynamic.
7. The use of this function

```
import { cn } from "lib/utils"

const state = true


<Button variant="ghost" className={cn(
    "bg-indigo-500",
    state && "bg-red-500"
)}>
    Click me
</Button>

```
the color of button will be red.


## Folder structure

1. add a specific font in the project, and that is Open_Sans, change in layout.tsx file.
2. To create new route we have to create new folder in the app directory.
3. What if i want to create a folder which is just for organising the code or structure of the project. So the solution in using (). like (auth)
4. create login and register folder in the (auth) folder create there respective pages. After that create (routes) folder in the (auth) folder and shift both login and register folder in the (routes) folder and we will be facing a problem with the files, There is nothing wrong that is just cache problem of next js.
5. The solution of this situation is to stop the server and delete the .next folder in the root directory, and restart again.

6. create a (main) folder in the app dir and create (routes) folder inside it, So will be facing the same problem and fix it.

## Authentication

1. For authentication we will be using Clerk.
2. We need to make some routes protected by the authentication.
3. First go to .gitignore file and add .env
4. Go to clerk.com and copy the env credentials.
5. We are not going to use default environment structure but we will be using dotenv becuase it will be helpfull for us for other libraries.
6. Setup Clerk in the project for auth.
7. run the command npm install @clerk/nextjs.
8. Mount the clerk provider to root layout.
9. Add middleware file to actually protects our routes.
10. create a new file middleware.ts
11. Copy the code from the docs and paste it in middleware.ts file.
12. Create the folders of sign-in and sign-up following the documentation and paste the respective code there.
13. copy the environment variables from the documentation and paste it in the .env file.
14. Run the application and what we find is that the register page is automatically opened after running the server.
15. Make changes in the layout.tsx file in (auth) to make the component center.
16. Add UserButton in page.tsx file as mentioned in the docs for sign out. The code is mentioned below for refrence.
```
<UserButton 
    afterSignOutUrl='/'
/>
```
## Dark and light Theme setup
1. to make this work we have to install a package named next theme.
2. npm install next-themes
3. create a new folder providers in the components folder to differentiate which are from provider and which are our components.
4. Create a new file theme-provider.tsx and paste the code mentioned in the documentation.
5. Wrap { children } in <ThemeProvider> component as mentioned in docs.
6. ```
    <ClerkProvider>
      <html lang="en" suppressHydrationWarning>
        <body className={font.className}>
          <ThemeProvider
            attribute='class'
            defaultTheme='dark'
            enableSystem={false}
            storageKey='discord-theme'
          >
            {children}
          </ThemeProvider>
        </body>
      </html>
    </ClerkProvider>
```
7. Add a toggle button to switch the themes.
8. Create a file in components directory named mode-toggle.tsx.
9. Add dropdown menu component from shadcn ui.
10. npx shadcn-ui@latest add dropdown-menu
11. Add <ModeToggle /> in the page.tsx file.
12. Made a change in the body element 
```
<body className={cn(font.className, "bg-white dark:bg-[#313338]"
)}>
```

## Database and Prisma Schema

1. Lets add some packages.
2. npm install -D prisma.
3. npx prisma init.
4. So now we have a folder named prisma and file named schema.prisma, Here we will create the db schema.
5. add postgresql db configuration by copying from neon tech dashboard and paste it in the environment file.
6. Make changes in schema.prisma file.
```
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
  relationMode = "prisma"
}
```

7. Create the initial DB Schema and the code is mentioned below

```
model Profile {
  id String @id @default(uuid())
  userId String @unique
  name String
  imageUrl String @db.Text
  email String @db.Text

  servers Server[]
  members Member[]
  channels Channel[]

  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

}

model Server {
  id String @id @default(uuid())
  name String 
  imageUrl String @db.Text
  inviteCode String @db.Text

  profileId String
  profile Profile @relation(fields: [profileId], references: [id], onDelete: Cascade)

  members Member[]
  channels Channel[]

  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([profileId])
}

enum MemberRole {
  ADMIN
  MODERATOR
  GUEST
}

model Member {
  id String @id @default(uuid())
  role MemberRole @default(GUEST)

  profileId String
  profile Profile @relation(fields: [profileId], references: [id], onDelete: Cascade)

  serverId String
  server Server @relation(fields: [serverId], references: [id], onDelete: Cascade)

  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([profileId])
  @@index([serverId])
}

enum ChannelType {
  TEXT
  AUDIO
  VIDEO
}

model Channel {
  id String @id @default(uuid())
  name String
  type ChannelType @default(TEXT)

  profileId String
  profile Profile @relation(fields: [profileId], references: [id], onDelete: Cascade)

  serverId String
  server Server @relation(fields: [serverId], references: [id], onDelete: Cascade)

  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([profileId])
  @@index([serverId])
  
}
```
8. After this lets made the migrations to the DB with the following commands.
9. Everytime we modify our Schema we have to run these commands.
10. npx prisma generate.
11. npx prisma db push.
12. After successfully integrating with the db we will see this message.

```
Your database is now in sync with your Prisma schema.
```

13. We need to create a database util which we are going to use througout our api and server components.
14. But before that lets add npm install @prisma/client
15. Create a new file named db.ts in lib folder.
16. The code for the file is mentioned below.
```
import { PrismaClient } from "@prisma/client";

declare global {
    var prisma: PrismaClient | undefined;
}

export const db = globalThis.prisma || new PrismaClient();

if (process.env.NODE_ENV !== "production") globalThis.prisma = db

```
17. Now lets modify page.tsx file. 
18. We will add the logic for creating the profile once a user logged in. and not create another account.
19. We have to delete (main) folder and create a new one named (setup) and create a file named page.tsx and this will be the default one from now on.
20. So now we have to load the profile, So create a new file in the lib folder named initial-profile.ts.

```

import { currentUser, redirectToSignIn } from "@clerk/nextjs";
import { db } from "@/lib/db";

export const initialProfile = async () => {
    const user = await currentUser();

    if (!user) {
        return redirectToSignIn();
    }

    const profile = await db.profile.findUnique({
        where: {
            userId: user.id
        }
    })

    if (profile) {
        return profile
    }

    const newProfile = await db.profile.create({
        data: {
            userId: user.id,
            name: `${user.firstName} ${user.lastName}`,
            imageUrl: user.imageUrl,
            email: user.emailAddresses[0].emailAddress
        }
    })

    return newProfile
}
```

21. Now lets call above function in the (setup) page.tsx file.
22. In the page tsx file we will call the function initialProfile and if the we found the profile, we will find the server related to that user and if there is a server we will redirect the user to that server page, otherwise we will call the user to create a server.
```
import { initialProfile } from "@/lib/initial-profile";
import { db } from "@/lib/db";
import { redirect } from "next/navigation";


const SetupPage = async () => {

    const profile = await initialProfile();

    const server = await db.server.findFirst({
        where: {
            members: {
                some: {
                    profileId: profile.id
                }
            }
        }
    })

    if (server) {
        return redirect(`/servers/${server.id}`)
    }



    return (
        <div>
            Create a server
        </div>
    );
}
 
export default SetupPage;
```
23. To take the full experience we need to write the command in the second terminal 
```
npx prisma studio
``` 
it will open a dashboard where i can see all the db tables and details.
24. Here we can see we have only one user and even after refresh it is not creating duplicate user.

## Initial Modal UI

1. Now we have to create a modal for the ui.
2. To create a modal we need dialogue box component from shadcn ui.
3. npx shadcn-ui@latest add dialog
4. We will need an input component.
5. npx shadcn-ui@latest add input
6. We will be needing react hook form and zod for validations.
7. npx shadcn-ui@latest add form
8. So Create a folder inside components directory named modals and create file named initial-modal.tsx and import it into (setup)/page.tsx.
9. The final code for initial-modal.tsx is mentioned below.

```
"use client"

import * as z from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";

import {
	Dialog,
	DialogDescription,
	DialogFooter,
	DialogHeader,
	DialogTitle,
	DialogContent,
} from "@/components/ui/dialog";
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

const formSchema = z.object({
    name: z.string().min(1, {
        message: "Server name is required."
    }),
    imageUrl: z.string().min(1, {
        message: "Server image is required."
    })
})


export const InitialModal = () => {

    const form = useForm({
        resolver: zodResolver(formSchema),
        defaultValues: {
            name: "",
            imageUrl: "",
        }
    });

    const isLoading = form.formState.isSubmitting;

    const onSubmit = async (values: z.infer<typeof formSchema>) => {
        console.log(values)
    }


    return (
        <Dialog open={true}>
            <DialogContent className="bg-white text-black p-0 overflow-hidden">
                <DialogHeader className="pt-8 px-6">
                    <DialogTitle className="text-2xl text-center font-bold">
                        Customize your server
                    </DialogTitle>
                    <DialogDescription className="text-center text-zinc-500">
                        Give your server a personality with a name and an image. You can always change it later.
                    </DialogDescription>
                </DialogHeader>
                <Form {...form}>
                    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
                        <div className="space-y-8 px-6">

                            <div className="flex items-center justify-center text-center">
                                TODO: Image Upload
                            </div>

                            <FormField
                                control={form.control}
                                name="name"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel
                                            className="uppercase text-xs font-bold text-zinc-500 dark:text-secondary/70"
                                        >
                                            Server name
                                        </FormLabel>
                                        <FormControl>
                                            <Input
                                                disabled={isLoading}
                                                className="bg-zinc-300/50 border-0 focus-visible:ring-0 text-black focus-visible:ring-offset-0"
                                                placeholder="Enter server name"
                                                {...field}
                                            />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                        </div>
                        <DialogFooter className="bg-gray-100 px-6 py-4">
                            <Button variant="primary" disabled={isLoading}>
                                Create
                            </Button>
                        </DialogFooter>

                    </form>
                </Form>
            </DialogContent>
        </Dialog>
    )
}
```
10. After this we need to add a variation to the button, So go to components/ui/button.tsx and add a variant.
11. add this variation in the button.tsx file.
```
primary: "bg-indigo-500 text-white hover:bg-indigo-500/90"
```
12. After implimenting we will be getting a hydration error, So lets fix it. Why this error is occuring, because of the modal and modals are notorious in nature and causes error.
13. So we have to apply mount technique and add a state, useEffect to see if the component is mounted or not.
```
  const [isMounted, setIsMounted] = useState(false)

  useEffect(() => {
      setIsMounted(true);
  }, [])

  if (!isMounted) {
        return null
    }  
```

## Setup the Uploadthing
1. lets visit uploadthing website.
2. login and create an app named discord_clone.
3. Copy the api keys and save it into your dot env file.
4. install the packages.
5. npm install uploadthing @uploadthing/react react-dropzone
6. To setup create a file in the following directory app/api/uploadthing/core.ts.
7. Now modify the code according to our needs.
8. final code for core.ts file is mentioned below.
```
import { auth } from "@clerk/nextjs"
import { createUploadthing, type FileRouter } from "uploadthing/next";

const f = createUploadthing();

const handleAuth = () => {
    const { userId } = auth();
    if (!userId) throw new Error("Unauthorized")
    return { userId: userId };
}

// const auth = (req: Request) => ({ id: "fakeId" }); // Fake auth function

// FileRouter for your app, can contain multiple FileRoutes
export const ourFileRouter = {
	serverImage: f({ image: { maxFileSize: "4MB", maxFileCount: 1 } })
        .middleware(() => handleAuth())
        .onUploadComplete(() => {}),
    messageFile: f(["image", "pdf"])
        .middleware(() => handleAuth())
        .onUploadComplete(() => {})
} satisfies FileRouter;

export type OurFileRouter = typeof ourFileRouter;

```
9. create a route.ts file as mentioned in the docs
```
import { createNextRouteHandler } from "uploadthing/next";

import { ourFileRouter } from "./core";

// Export routes for Next App Router
export const { GET, POST } = createNextRouteHandler({
	router: ourFileRouter,
});

```
10. create a uploadthing.ts file in lib folder.
```

import { generateComponents } from "@uploadthing/react";

import type { OurFileRouter } from "@/app/api/uploadthing/core";

export const { UploadButton, UploadDropzone, Uploader } =
	generateComponents<OurFileRouter>();
```
11. So, uploadthing is auth protected form uploading but we still need to add it in the authmiddleware. So, Open the middlewre.ts file and add public routes to avoid potential errors.
```
export default authMiddleware({
	publicRoutes: ["/api/upladthing"]
});
```

12. Now lets modify initial-modal.tsx file for uploadthing.
13. Create a component named file-upload.tsx in components folder.
14. add this code in initial-modal-.tsx file in the TODO.

```
<FormField
    control={form.control}
    name="imageUrl"
    render={({field}) => (
      <FormItem>
        <FormControl>
          <FileUpload
            endpoint="serverImage"
            value={field.value}
            onChange={field.onChange}
          />
        </FormControl>
      </FormItem>
    )}
  />
```

15. So add the following code in the file-upload.tsx file.
```
"use client";

import { X } from "lucide-react";
import Image from "next/image";
import { UploadDropzone } from "@/lib/uploadthing";
import "@uploadthing/react/styles.css"



interface FileUploadProps {
    onChange: (url?: string) => void;
    value: string;
    endpoint: "messageFile" | "serverImage"
}


export const FileUpload = ({
    onChange,
    value,
    endpoint
}: FileUploadProps) => {

    const fileType = value?.split(".").pop();
    if (value && fileType !== "pdf") {
        return (
            <div className="relative h-20 w-20">
                <Image
                    fill
                    src={value}
                    alt="Upload"
                    className="rounded-full"
                />
            </div>
        )
    }

    return (
        <UploadDropzone
            endpoint={endpoint}
            onClientUploadComplete={(res) => {
                onChange(res?.[0].url)
            }}
            onUploadError={(error: Error) => {
                console.log(error)
            }}
        />
    )
}
```

16. After implimenting this code we will be getting an error related to next.config.ts file to include image in it.
17. So to resolve this error we need to include this code in the next.config.js file.
```
/** @type {import('next').NextConfig} */
const nextConfig = {
    images: {
        domains: [
            "uploadthing.com",
            "utfs.io"
        ]
    }
}

module.exports = nextConfig
```
18. After this we need to add a remove button to remove image from the component.
19. The final code for file-upload.tsx file is mentioned below.

```
"use client";

import { X } from "lucide-react";
import Image from "next/image";
import { UploadDropzone } from "@/lib/uploadthing";
import "@uploadthing/react/styles.css"



interface FileUploadProps {
    onChange: (url?: string) => void;
    value: string;
    endpoint: "messageFile" | "serverImage"
}


export const FileUpload = ({
    onChange,
    value,
    endpoint
}: FileUploadProps) => {

    const fileType = value?.split(".").pop();
    if (value && fileType !== "pdf") {
        return (
            <div className="relative h-20 w-20">
                <Image
                    fill
                    src={value}
                    alt="Upload"
                    className="rounded-full"
                />
                <button
                    onClick={() => onChange("")}
                    className="bg-rose-500 text-white p-1 rounded-full absolute top-0 right-0 shadow-sm"
                    type="button"
                >
                    <X className="h-4 w-4" />
                </button>
            </div>
        )
    }

    return (
        <UploadDropzone
            endpoint={endpoint}
            onClientUploadComplete={(res) => {
                onChange(res?.[0].url)
            }}
            onUploadError={(error: Error) => {
                console.log(error)
            }}
        />
    )
}

```
20. Next Step is to send the data to backend and create a server for the user.


## Server Creation api.

1. We need to make changes in intial-modal.tsx file to call the api.
2. lets install some packages.
3. npm install axios.
4. change the onSubmit function code to this and also we need to use the router provided by next js.
```
import { useRouter } from "next/navigation";
const router = useRouter()
const onSubmit = async (values: z.infer<typeof formSchema>) => {
		try {
			await axios.post("/api/servers", values)

			form.reset();
			router.refresh();
			window.location.reload();

		} catch (error) {
			console.log(error)
		}
	};

```
5. Now lets create the api calls for the server, So create server folder inside api folder and create a route.ts file in it.
6. But before that lets create a util which we will be using accross all our routes and server components to check current profile, So create a new file in lib folder named current-profile.ts.
7. add this code in current-profile.tsx file.

```
import { auth } from "@clerk/nextjs";

import { db } from "@/lib/db";

export const currentProfile = async () => {
    const { userId } = auth();
    if (!userId) {
        return null
    }

    const profile = await db.profile.findUnique({
        where: {
            userId
        }
    })

    return profile
}
```

8. Now lets work in route.ts file.
9. install a package named npm install uuid 
10. npm install -D @types/uuid
11. The final code for route.ts file for creating the server is mentioned below 
```
import {v4 as uuidv4} from "uuid";
import { NextResponse } from "next/server";
import { currentProfile } from "@/lib/current-profile";
import { db } from "@/lib/db";
import { MemberRole } from "@prisma/client";


export async function POST(req: Request) {
    try {
        const { name, imageUrl } = await req.json();
        const profile = await currentProfile();

        if (!profile) {
            return new NextResponse("Unauthorized", {status: 401})
        }

        const server = await db.server.create({
            data: {
                profileId: profile.id,
                name,
                imageUrl,
                inviteCode: uuidv4(),
                channels: {
                    create: [
                        {name: "general", profileId: profile.id}
                    ]
                },
                members: {
                    create: [
                        {profileId: profile.id, role: MemberRole.ADMIN}
                    ]
                }
            }
        })

        return NextResponse.json(server)

        
    } catch (error) {
        console.log("[SERVERS_POST]", error)
        return new NextResponse("Internal Error", {status: 500})
    }
}
```
12. After successfully testing the creation of server we will be going to a 404 page, because right now there is no server page in the application, So now we need to create a view which will render the server page.

## Navigation Sidebar

1. After creating the page inside (main)/(routes)/servers/[serverId] route we will have no longer the error of 404.
2. create a layout.tsx file in (main) folder and here is the initial code for it.
```
const MainLayout = async ({
    children
}: {
    children: React.ReactNode
}) => {
    return (
        <div className="h-full">
            <div className="hidden md:flex h-full w-[72px] z-30 flex-col fixed inset-y-0">
                <NavigationSidebar />
            </div>
            <main className="md:pl-[72px] h-full">
                {children}
            </main>
        </div>
    )
}

export default MainLayout;

``` 
3. We have to include a component named NavigationSidebar, create a folder named navigation in components and create the file named navigation-sidebar.tsx.
4. So this is the initial structure for navigation-sidebar.tsx file.
```
import { redirect } from "next/navigation";

import { currentProfile } from "@/lib/current-profile";
import { db } from "@/lib/db";

export const NavigationSidebar = async () => {

    const profile = await currentProfile();
    if (!profile) {
        return redirect("/")
    }

    const servers = await db.server.findMany({
        where: {
            members: {
                some: {
                    profileId: profile.id
                }
            }
        }
    });



    return (
        <div className="space-y-4 flex flex-col items-center h-full text-primary w-full dark:bg-[#1E1F22] py-3">
            navigation sidebar
        </div>
    )
}
```
5. Now we need to create a navigation action component.
6. So we need to install a package from shadcn.
7. npx shadcn-ui@latest add tooltip
8. npx shadcn-ui@latest add separator
9. We need to create an NavigationAction Component, So create component named navigation-action.tsx and include this component in navigation-sidebar component.
10. this is the initial code till now for navigation-action.tsx file.

```
"use client";

import { Plus } from "lucide-react";

export const NavigationAction = () => {
    return (
        <div>
            <button
                className="group flex items-center"
            >
                <div className="flex mx-3 h-[48px] w-[48px] rounded-[24px] group-hover:rounded-[16px] transition-all overflow-hidden items-center justify-center bg-background dark:bg-neutral-700 group-hover:bg-emerald-500">
                    <Plus
                        className="group-hover:text-white transition text-emerald-500"
                        size={25}
                    />
                </div>
            </button>
        </div>
    )
}
```

11. Now we have to add the tooltip.So, create a file named action-tooltip.tsx in components folder.
12. The initial code for the tooltip is mentioned below and include it into navigation-action.tsx file.
```
"use client";

import {
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger
} from "@/components/ui/tooltip";

interface ActionTooltipProps {
    label: string;
    children: React.ReactNode;
    side?: "top" | "right" | "bottom" | "left";
    align: "start" | "center" | "end";
}


export const ActionTooltip = ({
    label,
    children,
    side,
    align
}: ActionTooltipProps) => {
    return (
        <TooltipProvider>
            <Tooltip delayDuration={50}>
                <TooltipTrigger asChild>
                    {children}
                </TooltipTrigger>
                <TooltipContent side={side} align={align}>
                    <p className="font-semibold text-sm capitalize">
                        {label.toLowerCase()}
                    </p>
                </TooltipContent>
            </Tooltip>
        </TooltipProvider>
    )
}

```

13. Wrap the navigation action inside <ActionTooltip></ActionTooltip> like mentioned below 
```
<ActionTooltip 
    side="right"
    align="center"
    label="Add a server"
>
    <button className="group flex items-center">
        <div className="flex mx-3 h-[48px] w-[48px] rounded-[24px] group-hover:rounded-[16px] transition-all overflow-hidden items-center justify-center bg-background dark:bg-neutral-700 group-hover:bg-emerald-500">
            <Plus
                className="group-hover:text-white transition text-emerald-500"
                size={25}
            />
        </div>
    </button>
</ActionTooltip>
```

14. Right now we are done with this button in future it will trigger a modal to open and create a new server. till then lets work on showing the server we have.
15. So add Separator in navigation-sidebar.tsx file.
```
<Separator
    className="h-[2px] bg-zinc-300 dark:bg-zinc-700 rounded-md w-10 mx-auto"
/>
```

16. Now we have to add a new component from shadcn ui and it is scroll area.
17. npx shadcn-ui@latest add scroll-area
18. add this scroll area in navigation-sidebar.tsx and create a components named navigation-item.tsx which will include in scrollarea.

19. navigation-sidebar updated code
```
<ScrollArea className="flex-1 w-full">
    {servers.map((server) => {
        return (
            <div key={server.id} className="mb-4">
                <NavigationItem
                    id={server.id}
                    name={server.name}
                    imageUrl={server.imageUrl}
                />
            </div>
        )
    })}
</ScrollArea>
```

20. navigation-item initial code.

```
"use client";

import Image from "next/image";
import { useParams, useRouter } from "next/navigation";

import { cn } from "@/lib/utils";
import { ActionTooltip } from "@/components/action-tooltip";


interface NavigationItemProps {
    id: string;
    imageUrl: string;
    name: string;
}

export const NavigationItem = ({
    id,
    imageUrl,
    name
}: NavigationItemProps) => {
    return (
        <div>
            server
        </div>
    )
}
```

21. This is the final code after displaying the data of server on the left side of navigation-item.tsx file.
```
"use client";

import Image from "next/image";
import { useParams, useRouter } from "next/navigation";

import { cn } from "@/lib/utils";
import { ActionTooltip } from "@/components/action-tooltip";


interface NavigationItemProps {
    id: string;
    imageUrl: string;
    name: string;
}

export const NavigationItem = ({
    id,
    imageUrl,
    name
}: NavigationItemProps) => {
    const params = useParams();

    const router = useRouter();

    const onClick = () => {
        router.push(`/servers/${id}`)
    }

    return (
        <ActionTooltip
            side="right"
            align="center"
            label={name}
        >
            <button
                onClick={onClick}
                className="group relative flex items-center"
            >
                <div className={cn(
                    "absolute left-0 bg-primary rounded-r-full transition-all w-[4px]",
                    params?.serverId !== id && "group-hover:h-[20px]",
                    params?.serverId === id ? "h-[36px]" : "h-8px"
                )} />
                <div className={cn(
                    "relative group flex mx-3 h-[48px] w-[48px] rounded-[24px] group-hover:rounded-[16px] transition-all overflow-hidden",
                    params?.serverId === id && "bg-primary/10 text-primary rounded-[16px]"
                )}>
                    <Image
                        fill
                        src={imageUrl}
                        alt="channel"
                    />
                </div>
            </button>
        </ActionTooltip>
    )
}
```

22. Add mode toggle and userButton component to navigation-sidebar.tsx file.
```
<div className="pb-3 mt-auto flex items-center flex-col gap-y-4">
    <ModeToggle />
    <UserButton
        afterSignOutUrl="/"                
        appearance={{
            elements: {
                avatarBox: "h-[48px] w-[48px]"
            }
        }}
    />
</div>

```
## Create Server Modal. 
1. add this class to mode-toggle component in the button tag
```
<Button className="bg-transparent border-0" variant="outline" size="icon">
```
2. Lets install zustand so that we can work with our modals.
3. npm install zustand
4. So, we will create a modal store where we will store the global state of the modal.
5. create a folder in root directory named hooks and create a file named use-modal-store.ts to control all modal in our application.
6. initial code for the modal hook.
```
import { create } from "zustand";

export type ModalType = "createServer";


interface ModalStore {
    type: ModalType | null;
    isOpen: boolean;
    onOpen: (type: ModalType) => void;
    onClose: () => void;
}

export const useModal = create<ModalStore>((set) => ({
    type: null,
    isOpen: false,
    onOpen: (type) => set({isOpen: true, type}),
    onClose: () => set({type: null, isOpen: false})
}))
```

7. Now lets create our create server modal.
8. Create a file named create-server-modal.tsx in components/modals and create a provider file named modal-provider.tsx in providers folder.
Provder file code.
```
"use client";

import { CreateServerModal } from "@/components/modals/create-server-modal";
import { useEffect, useState } from "react";


export const ModalProvider = () => {
    const [isMounted, setIsMounted] = useState(false)

    useEffect(() => {
        setIsMounted(true)
    }, [])

    if (!isMounted) {
        return null;
    }

    return (
        <>
            <CreateServerModal />
        </>
    )
}
```
9. initial code for create-server-modal.tsx file.
```
"use client";

import * as z from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import axios from "axios";

import {
	Dialog,
	DialogDescription,
	DialogFooter,
	DialogHeader,
	DialogTitle,
	DialogContent,
} from "@/components/ui/dialog";
import {
	Form,
	FormControl,
	FormField,
	FormItem,
	FormLabel,
	FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

import { FileUpload } from "@/components/file-upload";
import { useRouter } from "next/navigation";
import { useModal } from "@/hooks/use-modal-store";

const formSchema = z.object({
	name: z.string().min(1, {
		message: "Server name is required.",
	}),
	imageUrl: z.string().min(1, {
		message: "Server image is required.",
	}),
});

export const CreateServerModal = () => {
	const {isOpen, onClose, type} = useModal();

	const router = useRouter();

    const isModalOpen = isOpen && type ==="createServer"

	

	const form = useForm({
		resolver: zodResolver(formSchema),
		defaultValues: {
			name: "",
			imageUrl: "",
		},
	});

	const isLoading = form.formState.isSubmitting;

	const onSubmit = async (values: z.infer<typeof formSchema>) => {
		try {
			await axios.post("/api/servers", values);

			form.reset();
			router.refresh();
		} catch (error) {
			console.log(error);
		}
	};

    const handleClose = () => {
        form.reset();
        onClose();
    }

	return (
		<Dialog open={isModalOpen} onOpenChange={handleClose}>
			<DialogContent className="bg-white text-black p-0 overflow-hidden">
				<DialogHeader className="pt-8 px-6">
					<DialogTitle className="text-2xl text-center font-bold">
						Customize your server
					</DialogTitle>
					<DialogDescription className="text-center text-zinc-500">
						Give your server a personality with a name and an image.
						You can always change it later.
					</DialogDescription>
				</DialogHeader>
				<Form {...form}>
					<form
						onSubmit={form.handleSubmit(onSubmit)}
						className="space-y-8"
					>
						<div className="space-y-8 px-6">
							<div className="flex items-center justify-center text-center">
								<FormField
									control={form.control}
									name="imageUrl"
									render={({ field }) => (
										<FormItem>
											<FormControl>
												<FileUpload
													endpoint="serverImage"
													value={field.value}
													onChange={field.onChange}
												/>
											</FormControl>
										</FormItem>
									)}
								/>
							</div>

							<FormField
								control={form.control}
								name="name"
								render={({ field }) => (
									<FormItem>
										<FormLabel className="uppercase text-xs font-bold text-zinc-500 dark:text-secondary/70">
											Server name
										</FormLabel>
										<FormControl>
											<Input
												disabled={isLoading}
												className="bg-zinc-300/50 border-0 focus-visible:ring-0 text-black focus-visible:ring-offset-0"
												placeholder="Enter server name"
												{...field}
											/>
										</FormControl>
										<FormMessage />
									</FormItem>
								)}
							/>
						</div>
						<DialogFooter className="bg-gray-100 px-6 py-4">
							<Button variant="primary" disabled={isLoading}>
								Create
							</Button>
						</DialogFooter>
					</form>
				</Form>
			</DialogContent>
		</Dialog>
	);
};

```

10. After that lets add this provider in the root layout.
```
<ClerkProvider>
    <html lang="en" suppressHydrationWarning={true}>
    <body className={cn(
        font.className,
        "bg-white dark:bg-[#313338]"
        )}>
        <ThemeProvider
        attribute='class'
        defaultTheme='dark'
        enableSystem={false}
        storageKey='discord-theme'
        >
        <ModalProvider />
            {children}
        </ThemeProvider>
    </body>
    </html>
</ClerkProvider>
```

11. Now lets add the functionality on the click of Plus button to open the modal.
12. Add this code in navigation-action.tsx file
```
import { useModal } from "@/hooks/use-modal-store";
const { onOpen } = useModal();
<button
    onClick={() => onOpen("createServer")}
    className="group flex items-center"
>
```
============  IMPORTANT  ==============

13. After this we will be getting an error that sidebar will not show on the screen.So , the solution of the problem is to shift the uploadthing css to global.css. 
Step 1 :-
- Remove the import for upload-thing styles inside file-upload.tsx component
- DELETE => import "@uploadthing/react/styles.css";

Step 2 :-
- Add the import at the bottom of the globals.css file instead
// globals.css
...
@import "~@uploadthing/react/styles.css";

Step 3 (optional):
- Wrap the tailwind config with "withUt":
// tailwind.config.js

const { withUt } = require("uploadthing/tw");
module.exports = withUt({
   ...leave everything the same
});

## Server Sidebar

1. So, now we have to create a sidebar in the server page where we can show all the channels related to that particular server.
2. Create the layout.tsx file inside [serverId] folder.
3. The below mentioned code is the basic layout of the page.
```
import { currentProfile } from "@/lib/current-profile";
import { db } from "@/lib/db";
import { redirectToSignIn } from "@clerk/nextjs";
import { redirect } from "next/navigation";


const ServerIdLayout = async ({
    children,
    params
}: {
    children: React.ReactNode,
    params: {serverId: string};
}) => {
    const profile = await currentProfile();

    if (!profile) {
        return redirectToSignIn();
    }

    const server = await db.server.findUnique({
        where: {
            id: params.serverId,
            members: {
                some: {
                    profileId: profile.id
                }
            }
        }
    })

    if (!server) {
        return redirect("/")
    }

    return (
		<div className="h-full">
			<div className="hidden md:flex h-full w-60 z-20 flex-col fixed inset-y-0">
                Server Sidebar
            </div>
			<main className="h-full md:pl-60">
                {children}
            </main>
		</div>
	);
}

export default ServerIdLayout;
```
4. We have to create a different component for this server sidebar.
5. So create a new folder inside components named server and create server-sidebar.tsx file and inclde this components in layout.tsx file <ServerSidebar />.
6. we have to get current profile in layout as well as ServerSidebar component because we are going to use these in mobile age also.
7. give serverId as a prop to server-sidebar component. <ServerSidebar serverId={params.serverId} />
8. create server-header.tsx file inside components/server directory and include it in server-sidebar.tsx.
9. We have to make a different type file for server details type becuase we are populating it with multiple children data.
10. So, Below mentioned is the code for server-sidebar.tsx.
```
import { currentProfile } from "@/lib/current-profile";
import { db } from "@/lib/db";
import { ChannelType } from "@prisma/client";
import { redirect } from "next/navigation";

import { ServerHeader } from "./server-header";

interface ServerSidebarProps {
    serverId: string;
}



export const ServerSidebar = async ({serverId} : ServerSidebarProps) => {
    const profile = await currentProfile();

    if (!profile) {
        return redirect("/");
    }

    const server = await db.server.findUnique({
        where: {
            id: serverId,
        },
        include: {
            channels: {
                orderBy: {
                    createdAt: "asc",
                }
            },
            members: {
                include: {
                    profile: true,
                },
                orderBy: {
                    role: "asc",
                }
            }
        }
    });


    const textChannels = server?.channels.filter((channel) => channel.type === ChannelType.TEXT)
    const audioChannels = server?.channels.filter((channel) => channel.type === ChannelType.AUDIO)
    const videoChannels = server?.channels.filter((channel) => channel.type === ChannelType.VIDEO)

    const members = server?.members.filter((member) => member.profileId !== profile.id)


    if (!server) {
        return redirect("/")
    }

    const role = server.members.find((member) => member.profileId === profile.id)?.role;

    return (
        <div className="flex flex-col h-full text-primary w-full dark:bg-[#2B2D31] bg-[#F2F3F5]">
            <ServerHeader server={server} role={role} />
        </div>
    )
}
```
11. Below mentioned is the code for server-header.tsx.
```
"use client";

import { ServerWithMembersWithProfiles } from "@/types";
import { MemberRole } from "@prisma/client";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { ChevronDown, LogOut, PlusCircle, Settings, Trash, UserPlus, Users } from "lucide-react";

interface ServerHeaderProps {
    server: ServerWithMembersWithProfiles;
    role?: MemberRole 
}

export const ServerHeader = ({
    server,
    role
}: ServerHeaderProps) => {
    const isAdmin = role === MemberRole.ADMIN;
    const isModerator = isAdmin || role === MemberRole.MODERATOR;

    return (
		<DropdownMenu>
			<DropdownMenuTrigger className="focus:outline-none" asChild>
				<button className="w-full text-md font-semibold px-3 flex items-center h-12 border-neutral-200 dark:border-neutral-800 border-b-2 hover:bg-zinc-700/10 dark:hover:bg-zinc-700/50 transition">
					{server.name}
					<ChevronDown className="h-5 w-5 ml-auto" />
				</button>
			</DropdownMenuTrigger>
			<DropdownMenuContent className="w-56 text-xs font-medium text-black dark:text-neutral-400 space-y-[2px]">
				{isModerator && (
					<DropdownMenuItem className="text-indigo-600 dark:text-indigo-400 px-3 py-2 text-sm cursor-pointer">
						Invite People
						<UserPlus className="h-4 w-4 ml-auto" />
					</DropdownMenuItem>
				)}
				{isAdmin && (
					<DropdownMenuItem className="px-3 py-2 text-sm cursor-pointer">
						Server Settings
						<Settings className="h-4 w-4 ml-auto" />
					</DropdownMenuItem>
				)}
				{isAdmin && (
					<DropdownMenuItem className="px-3 py-2 text-sm cursor-pointer">
						Manage Memebers
						<Users className="h-4 w-4 ml-auto" />
					</DropdownMenuItem>
				)}
				{isModerator && (
					<DropdownMenuItem className="px-3 py-2 text-sm cursor-pointer">
						Create Channel
						<PlusCircle className="h-4 w-4 ml-auto" />
					</DropdownMenuItem>
				)}
				{isModerator && <DropdownMenuSeparator />}
				{isAdmin && (
					<DropdownMenuItem className="text-rose-500 px-3 py-2 text-sm cursor-pointer">
						Delete Server
						<Trash className="h-4 w-4 ml-auto" />
					</DropdownMenuItem>
				)}
				{!isAdmin && (
					<DropdownMenuItem className="text-rose-500 px-3 py-2 text-sm cursor-pointer">
                        Leave Server
						<LogOut className="h-4 w-4 ml-auto" />
					</DropdownMenuItem>
				)}
			</DropdownMenuContent>
		</DropdownMenu>
	);   
}
```
12. below mentiooned is the code for types file which is created in the root directory named types.ts.
```
import {Server, Member, Profile} from "@prisma/client";


export type ServerWithMembersWithProfiles = Server & {
    members: (Member & { profile: Profile })[];
}
```
## Invitations

1. So, Now we will create modals for all the features that we have mentioned above.
2. Lets first Work on invite modal.
3. add type, interface and data in hook.
```
export type ModalType = "createServer" | "invite";

interface ModalData {
    server?: Server
}


interface ModalStore {
    type: ModalType | null;
    data: ModalData
    isOpen: boolean;
    onOpen: (type: ModalType, data?: ModalData) => void;
    onClose: () => void;
}

export const useModal = create<ModalStore>((set) => ({
    type: null,
    data: {},
    isOpen: false,
    onOpen: (type, data = {}) => set({isOpen: true, type, data}),
    onClose: () => set({type: null, isOpen: false})
}))
```
4. use This hook in server-header.tsx file.
```
const { onOpen } = useModal();
<DropdownMenuItem
    onClick={() => onOpen("invite", { server:server })}
    className="text-indigo-600 dark:text-indigo-400 px-3 py-2 text-sm cursor-pointer"
    >
    Invite People
    <UserPlus className="h-4 w-4 ml-auto" />
</DropdownMenuItem>
```
5. Now lets create the invite modal. Create a file named invite-modal.tsx in components/modals.
6. add this model component in the modal provider.
7. Below mentioned is the basic layout of invite modal.
```
"use client";

import {
	Dialog,
	DialogHeader,
	DialogTitle,
	DialogContent,
} from "@/components/ui/dialog";
import { useModal } from "@/hooks/use-modal-store";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Copy, RefreshCw } from "lucide-react";



export const InviteModal = () => {
	const { isOpen, onClose, type } = useModal();

	const isModalOpen = isOpen && type === "invite";

	

	return (
		<Dialog open={isModalOpen} onOpenChange={onClose}>
			<DialogContent className="bg-white text-black p-0 overflow-hidden">
				<DialogHeader className="pt-8 px-6">
					<DialogTitle className="text-2xl text-center font-bold">
						Invite friends
					</DialogTitle>		
				</DialogHeader>
                <div className="p-6">
                    <Label
                        className="uppercase text-xs font-bold text-zinc-500 dark:text-secondary/70"
                    >
                        Server invite link
                    </Label>
                    <div className="flex items-center mt-2 gap-x-2">
                        <Input
                            className="bg-zinc-300/50 border-0 focus-visible:ring-0 text-black focus-visible:ring-offset-0"
                            value="invite-link"
                        />
                        <Button size="icon">
                            <Copy
                                className="w-4 h-4"
                            />
                        </Button>
                    </div>
                    <Button
                        variant='link'
                        size="sm"
                        className="text-xs text-zinc-500 mt-4"
                    >
                        Generate a new link
                        <RefreshCw
                            className="w-4 h-4 ml-2"
                        />
                    </Button>
                </div>
			</DialogContent>
		</Dialog>
	);
};

```
8. Now lets create a hook to read the current url. create a new file named use-origin.ts in the hooks folder.
```
import { useEffect, useState } from "react"

export const useOrigin = () => {
    const [mounted, setMounted] = useState(false)

    useEffect(() => {
        setMounted(true)
    }, [])

    const origin = typeof window !== "undefined" && window.location.origin ? window.location.origin : ""

    if (!mounted) {
        return "";
    }

    return origin

}
```
9. Now lets use this hook in invite modal.
10. So What is the scenario now, we have to create two new states copied and isLoading, create onCopy function which will copy the text to clipboard and onNew() function which will update the invite code, below mentioned are the changes we need to make in the invitte-modal.tsx file and add isLoading to button.
```
const { isOpen, onClose, type, data, onOpen } = useModal();
const [copied, setCopied] = useState(false)
const [isLoading, setIsLoading] = useState(false);

const onCopy = () => {
    navigator.clipboard.writeText(inviteUrl);
    setCopied(true)

    setTimeout(() => {
        setCopied(false)
    }, 1000);
}

const onNew = async () => {
    try {
        setIsLoading(true)
        const response = await axios.patch(`/api/servers/${server?.id}/invite-code`);
        onOpen("invite", {server: response.data})
    } catch (error) {
        console.log(error)
    } finally {
        setIsLoading(false)
    }
}

<Button size="icon" onClick={onCopy} disabled={isLoading}>
    {copied ? (
        <Check className="w-4 h-4" />
    ) : (
        <Copy className="w-4 h-4" />
    )}
</Button>

```
11. after this if we try to click on generate new link we will be getting an axios error 404.
12. create this folder structure api/servers/[serverId]/invite-code/route.ts and the code is mentioned below.
```
import { currentProfile } from "@/lib/current-profile"
import { db } from "@/lib/db";
import { NextResponse } from "next/server"
import { v4 as uuidv4 } from 'uuid';

export async function PATCH(
    req: Request,
    {params} : {params: {serverId: string}}
) {
    try {
        const profile = await currentProfile();

        if (!profile) {
            return new NextResponse("Unauthorized", {status: 401})
        }

        if (!params.serverId) {
            return new NextResponse("Server ID Missing", {status: 400})
        }

        const server = await db.server.update({
            where: {
                id:params.serverId,
                profileId: profile.id,
            },
            data: {
                inviteCode: uuidv4(),
            }
        })

        return NextResponse.json(server);

    } catch (error) {
        console.log("[SERVER_ID]", error)
        return new NextResponse("Internal Error", {status: 500})
    }
}
```
13. after this we will be able to generate new invite code for the server but if copy it and give it to some user and he uses to enter a server he can not because he will be getting 404 error.
14. So lets fix this now.
15. Create this directory in the app folder (invite)/(routes)/invite/[inviteCode]/page.tsx.
16. Below mentioned is the code for above mentioned file.
```
import { currentProfile } from "@/lib/current-profile";
import { db } from "@/lib/db";

import { redirectToSignIn } from "@clerk/nextjs";
import { redirect } from "next/navigation";

interface InviteCodePageProps {
    params: {
        inviteCode: string;
    };
}



const InviteCodePage = async ({
    params
}: InviteCodePageProps) => {

    const profile = await currentProfile();

    if (!profile) {
        return redirectToSignIn();
    }

    if (!params.inviteCode) {
        return redirect("/")
    }

    const existingServer = await db.server.findFirst({
        where: {
            inviteCode: params.inviteCode,
            members: {
                some: {
                    profileId: profile.id
                }
            }
        }
    })

    if (existingServer) {
        return redirect(`/servers/${existingServer.id}`)
    }

    const server = await db.server.update({
        where: {
            inviteCode: params.inviteCode,
        },
        data: {
            members: {
                create: {
                    profileId: profile.id
                }
            }
        }
    })


    return (
        <div>
            Hello Invite
        </div>
    );
}
 
export default InviteCodePage;
```

17. We will be getting an error because of the db schema, So change the inviteCode to @unique and run the following commands.
npx prisma generate
npx prisma db push
18. It will make changes to the db. but since we are changing the key to unique key so it will generate a warning to delete all data of the server. For that we need to reset the database by writing these commands.
npx prisma migrate reset
npx prisma generate
npx prisma db push
and run the server again and it will bring us to home page where we need to create the server again.
19. updated code for the above mentioned file.
```
const server = await db.server.update({
    where: {
        inviteCode: params.inviteCode,
    },
    data: {
        members: {
            create: [
                {
                    profileId: profile.id,
                },
            ],
        },
    },
});

if (server) {
    return redirect(`/servers/${server.id}`);
}


return null;
```

## Server Setting Modal
1. Now we have to create server setting modal.
2. So go to hooks and use-modal-store.ts file.
3. add this
```
export type ModalType = "createServer" | "invite" | "editServer";
```
4. create a new file named edit-server-modal.tsx in the components/modal folder.
5. add this component to modal-provider.tsx file.
```
<CreateServerModal />
<InviteModal />
<EditServerModal />
```
6. open the server-header.tsx file and add onClick functionality to server settings line.
```
onClick={() => onOpen("editServer", {server})}
```
7. below mentioned is the code for edit-server-modal.tsx file.

```
"use client";

import * as z from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import axios from "axios";
import { useEffect } from "react";

import {
	Dialog,
	DialogDescription,
	DialogFooter,
	DialogHeader,
	DialogTitle,
	DialogContent,
} from "@/components/ui/dialog";
import {
	Form,
	FormControl,
	FormField,
	FormItem,
	FormLabel,
	FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

import { FileUpload } from "@/components/file-upload";
import { useRouter } from "next/navigation";
import { useModal } from "@/hooks/use-modal-store";


const formSchema = z.object({
	name: z.string().min(1, {
		message: "Server name is required.",
	}),
	imageUrl: z.string().min(1, {
		message: "Server image is required.",
	}),
});

export const EditServerModal = () => {
	const { isOpen, onClose, type, data } = useModal();

	const router = useRouter();

	const isModalOpen = isOpen && type === "editServer";
	const {server} = data;

	const form = useForm({
		resolver: zodResolver(formSchema),
		defaultValues: {
			name: "",
			imageUrl: "",
		},
	});

	useEffect(() => {
		if (server) {
			form.setValue("name", server.name);
			form.setValue("imageUrl", server.imageUrl)
		}
	}, [server, form])

	const isLoading = form.formState.isSubmitting;

	const onSubmit = async (values: z.infer<typeof formSchema>) => {
		try {
			await axios.patch(`/api/servers/${server?.id}`, values);

			form.reset();
			router.refresh();
			onClose();
		} catch (error) {
			console.log(error);
		}
	};

	const handleClose = () => {
		form.reset();
		onClose();
	};

	return (
		<Dialog open={isModalOpen} onOpenChange={handleClose}>
			<DialogContent className="bg-white text-black p-0 overflow-hidden">
				<DialogHeader className="pt-8 px-6">
					<DialogTitle className="text-2xl text-center font-bold">
						Customize your server
					</DialogTitle>
					<DialogDescription className="text-center text-zinc-500">
						Give your server a personality with a name and an image.
						You can always change it later.
					</DialogDescription>
				</DialogHeader>
				<Form {...form}>
					<form
						onSubmit={form.handleSubmit(onSubmit)}
						className="space-y-8"
					>
						<div className="space-y-8 px-6">
							<div className="flex items-center justify-center text-center">
								<FormField
									control={form.control}
									name="imageUrl"
									render={({ field }) => (
										<FormItem>
											<FormControl>
												<FileUpload
													endpoint="serverImage"
													value={field.value}
													onChange={field.onChange}
												/>
											</FormControl>
										</FormItem>
									)}
								/>
							</div>

							<FormField
								control={form.control}
								name="name"
								render={({ field }) => (
									<FormItem>
										<FormLabel className="uppercase text-xs font-bold text-zinc-500 dark:text-secondary/70">
											Server name
										</FormLabel>
										<FormControl>
											<Input
												disabled={isLoading}
												className="bg-zinc-300/50 border-0 focus-visible:ring-0 text-black focus-visible:ring-offset-0"
												placeholder="Enter server name"
												{...field}
											/>
										</FormControl>
										<FormMessage />
									</FormItem>
								)}
							/>
						</div>
						<DialogFooter className="bg-gray-100 px-6 py-4">
							<Button variant="primary" disabled={isLoading}>
								Save
							</Button>
						</DialogFooter>
					</form>
				</Form>
			</DialogContent>
		</Dialog>
	);
};

```
8. create a file in api/servers/[serverId]/route.ts and below is the code for it.
```
import { currentProfile } from "@/lib/current-profile"
import { db } from "@/lib/db";
import { NextResponse } from "next/server"

export async function PATCH(
    req: Request,
    { params }: {params: {serverId: string}}
){
    try {
        const profile = await currentProfile();

        const { name, imageUrl } = await req.json();

        if (!profile) {
            return new NextResponse("Unauthorized", {status: 404})
        }
        const server = await db.server.update({
            where : {
                id: params.serverId,
                profileId: profile.id
            },
            data: {
                name,
                imageUrl
            }
        })

        return NextResponse.json(server)


    } catch (error) {
        console.log("[SERVER_ID_PATCH]", error)
        return new NextResponse("Internal Error", {status: 500})
    }
}

```
9. Now we can test the functionality of editing the server.


## Manage Members

1. So now lets work on the manage members functionality.
2. let visit use modal store and add "members" to the type.
3. create a new file in components/modals named members-modal.tsx. and add this component to the modal-provider. tsx file.
4. Go to server-header.tsx file and add onClick function to manage members tag.
```
<DropdownMenuItem 
    onClick={() => onOpen("members", {server})}
    className="px-3 py-2 text-sm cursor-pointer"
>
    Manage Memebers
    <Users className="h-4 w-4 ml-auto" />
</DropdownMenuItem>
```
5. After making some changes to members-modal.tsx file, typescript will give an error on server.members because in the modal store we are only passing server, So to fix this error we have to use types.ts file and change the code for const {server}

```
const { server } = data as {server: ServerWithMembersWithProfiles};
```
6. The final code will be in the last but till then I will explain the steps in between.
7. after modifying the members-modal.tsx file we have to create a new component user-avatar.tsx file in the components folder.
8. install new shadcn library
npx shadcn-ui@latest add avatar
9. Till now this is the code for members-modal.tsx file in which we have showed the members in the server and user-avatar.tsx file which is used to show avatar of the user.
```
"use client";

import { useState } from "react";
import {
	Dialog,
	DialogHeader,
	DialogTitle,
	DialogContent,
	DialogDescription,
} from "@/components/ui/dialog";
import { useModal } from "@/hooks/use-modal-store";
import { ServerWithMembersWithProfiles } from "@/types";
import { ScrollArea } from "@/components/ui/scroll-area";
import { UserAvatar } from "@/components/user-avatar";
import { ShieldAlert, ShieldCheck } from "lucide-react";

const roleIconMap = {
	"GUEST" : null,
	"MODERATOR" : <ShieldCheck className="h-4 w-4 ml-2 text-indigo-500" />,
	"ADMIN" : <ShieldAlert className="h-4 w-4 text-rose-500" />
}

export const MembersModal = () => {
	const { isOpen, onClose, type, data, onOpen } = useModal();

	const isModalOpen = isOpen && type === "members";
    
	const { server } = data as {server: ServerWithMembersWithProfiles};


	return (
		<Dialog open={isModalOpen} onOpenChange={onClose}>
			<DialogContent className="bg-white text-black overflow-hidden">
				<DialogHeader className="pt-8 px-6">
					<DialogTitle className="text-2xl text-center font-bold">
						Manage Members
					</DialogTitle>
					<DialogDescription className="text-center text-zinc-500">
						{server?.members.length} Members
					</DialogDescription>
				</DialogHeader>

				<ScrollArea
					className="mt-8 max-h-[420px] pr-6"
				>
					{server?.members?.map((member) => {
						return (
							<div key={member.id} className="flex items-center gap-x-2 mb-6">
								<UserAvatar src={member.profile.imageUrl} />
								<div className="flex flex-col gap-y-1">
									<div className="text-xs font-semibold flex items-center gap-x-1">
										{member.profile.name}
										{roleIconMap[member.role]}
									</div>
									<p className="text-xs text-zinc-500">{member.profile.email}</p>
								</div>
							</div>
						)
					})}
				</ScrollArea>
			</DialogContent>
		</Dialog>
	);
};

```
10. Given below is the code for user-avatar.tsx file.
```
import { Avatar, AvatarImage } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";

interface UserAvatarProps {
    src? : string;
    className? : string;
};


export const UserAvatar = ({
    src,
    className
} : UserAvatarProps) => {
    return (
        <Avatar className={cn("h-7 w-7 md:h-10 md:w-10", className)}>
            <AvatarImage src={src} />
        </Avatar>
    )
}
```
11. Now we have to work on the options on the right side with which the admin can give permissions to user or make changes to the user.
12. we have to add Dropdown menu in the file and create functions which will change the role of users.
13. This is the updated code till now after adding role change function.
```
export const MembersModal = () => {
	const { isOpen, onClose, type, data, onOpen } = useModal();

	const [loadingId, setLoadingId] = useState("");

	const isModalOpen = isOpen && type === "members";
    
	const { server } = data as {server: ServerWithMembersWithProfiles};

	const onRoleChange = async (memberId: string, role: MemberRole) => {
		try {
			setLoadingId(memberId);
		} catch (error) {
			console.log(error);
		}finally {
			setLoadingId("");
		}
	}	


	return (
		<Dialog open={isModalOpen} onOpenChange={onClose}>
			<DialogContent className="bg-white text-black overflow-hidden">
				<DialogHeader className="pt-8 px-6">
					<DialogTitle className="text-2xl text-center font-bold">
						Manage Members
					</DialogTitle>
					<DialogDescription className="text-center text-zinc-500">
						{server?.members?.length} Members
					</DialogDescription>
				</DialogHeader>

				<ScrollArea
					className="mt-8 max-h-[420px] pr-6"
				>
					{server?.members?.map((member) => {
						return (
							<div
								key={member.id}
								className="flex items-center gap-x-2 mb-6"
							>
								<UserAvatar src={member.profile.imageUrl} />
								<div className="flex flex-col gap-y-1">
									<div className="text-xs font-semibold flex items-center gap-x-1">
										{member.profile.name}
										{roleIconMap[member.role]}
									</div>
									<p className="text-xs text-zinc-500">
										{member.profile.email}
									</p>
								</div>
								{server.profileId !== member.profileId &&
									loadingId !== member.id && (
										<div className="ml-auto">
											<DropdownMenu>
												<DropdownMenuTrigger>
													<MoreVertical className="h-4 w-4 text-zinc-500" />
												</DropdownMenuTrigger>
												<DropdownMenuContent side="left">
													<DropdownMenuSub>
														<DropdownMenuSubTrigger className="flex items-center">
															<ShieldQuestion className="w-4 h-4 mr-2" />
															<span>Role</span>
														</DropdownMenuSubTrigger>
														<DropdownMenuPortal>
															<DropdownMenuSubContent>
																<DropdownMenuItem>
																	<Shield className="h-4 w-4 mr-2" />
																	Guest
																	{member.role ===
																		"GUEST" && (
																		<Check className="h-4 w-4 ml-auto" />
																	)}
																</DropdownMenuItem>
																<DropdownMenuItem>
																	<ShieldCheck className="h-4 w-4 mr-2" />
																	Moderator
																	{member.role ===
																		"MODERATOR" && (
																		<Check className="h-4 w-4 ml-auto" />
																	)}
																</DropdownMenuItem>
															</DropdownMenuSubContent>
														</DropdownMenuPortal>
													</DropdownMenuSub>
													<DropdownMenuSeparator />
													<DropdownMenuItem>
														<Gavel className="h-4 w-4 mr-2" />
														Kick
													</DropdownMenuItem>
												</DropdownMenuContent>
											</DropdownMenu>
										</div>
									)}
									{loadingId === member.id && (
										<Loader2
											className="animate-spin text-zinc-500 ml-auto w-4 h-4"
										/>
									)}
							</div>
						);
					})}
				</ScrollArea>
			</DialogContent>
		</Dialog>
	);
};
```

14. Now lets add a package which will help us generating url queries.
15. npm install query-String
16. add useRouter hook to the code and modify the onRoleChange code to this
```
const onRoleChange = async (memberId: string, role: MemberRole) => {
    try {
        setLoadingId(memberId);
        const url = qs.stringifyUrl({
            url: `/api/members/${memberId}`,
            query: {
                serverId: server?.id,
                memberId,
            }
        });

        const response = await axios.patch(url, { role })

        router.refresh();
        onOpen("members", {server: response.data});

    } catch (error) {
        console.log(error);
    }finally {
        setLoadingId("");
    }
}
```
17. add onclick function to dropdownitem

```
<DropdownMenuItem
    onClick={() =>
        onRoleChange(
            member.id,
            "GUEST"
        )
    }
>
    <Shield className="h-4 w-4 mr-2" />
    Guest
    {member.role ===
        "GUEST" && (
        <Check className="h-4 w-4 ml-auto" />
    )}
</DropdownMenuItem>
<DropdownMenuItem
    onClick={() =>
        onRoleChange(
            member.id,
            "MODERATOR"
        )
    }
>
```

18. Now if test the change in roles we will get error 404 because the routes are not created till now.
19. create a folder in api named members and create route.ts file and below is the mentioned code for it.
```
import { currentProfile } from "@/lib/current-profile"
import { db } from "@/lib/db";
import { NextResponse } from "next/server"

export async function PATCH(
    req: Request,
    {params} : {params : {memberId: string}}
) {
    try {
        const profile = await currentProfile();

        const { searchParams } = new URL(req.url)
        const { role } = await req.json();

        const serverId = searchParams.get("serverId")

        if (!profile) {
            return new NextResponse("Unauthorized", {status: 401})
        }

        if(!serverId) {
            return new NextResponse("Server ID missing", {status: 400})
        }

        if (!params.memberId) {
            return new NextResponse("Member ID missing", {status: 400})
        }

        const server = await db.server.update({
            where: {
                id: serverId,
                profileId: profile.id,
            },
            data: {
                members: {
                    update: {
                        where: {
                            id: params.memberId,
                            profileId: {
                                not: profile.id
                            }
                        },
                        data: {
                            role
                        }
                    }
                }
            },
            include: {
                members: {
                    include: {
                        profile: true
                    },
                    orderBy: {
                        role: "asc"
                    }
                }
            }

        })

        return NextResponse.json(server);




    } catch (error) {
        console.log("[MEMBERS_ID_PATCH]", error)
        return new NextResponse("Internal Error", {status: 500})
    }
}
```

20. updated onRoleChange code given below
```
const onRoleChange = async (memberId: string, role: MemberRole) => {
		try {
			setLoadingId(memberId);
			const url = qs.stringifyUrl({
				url: `/api/members/${memberId}`,
				query: {
					serverId: server?.id,
				}
			});

			const response = await axios.patch(url, { role })

			router.refresh();
			onOpen("members", {server: response.data});

		} catch (error) {
			console.log(error);
		}finally {
			setLoadingId("");
		}
	}
```
21. Now lets work on kick option.
22. create a function in members/[memberId]/route.ts file the code is given below.
```
export async function DELETE(
    req: Request,
    {params} : {params: {memberId: string}}
) {
    try {
        const profile = await currentProfile();
        const {searchParams} = new URL(req.url)

        const serverId = searchParams.get("serverId")

        if (!profile) {
            return new NextResponse("Unauthorized", {status: 401})
        }

        if(!serverId) {
            return new NextResponse("Server ID Missing", {status: 400})
        }

        if (!params.memberId) {
            return new NextResponse("Member Id Missing", {status: 400})
        }

        const server = await db.server.update({
            where: {
                id: serverId,
                profileId: profile.id,
            },
            data: {
                members: {
                    deleteMany: {
                        id: params.memberId,
                        profileId: {
                            not: profile.id
                        }
                    }
                }
            },
            include: {
                members: {
                    include: {
                        profile: true,
                    },
                    orderBy: {
                        role: "asc",
                    }
                }
            }
        })

        return NextResponse.json(server)

    } catch (error) {
        console.log("[MEMBER_ID_DELETE]", error)
        return new NextResponse("Internal Error", {status: 500})
    }
}
```

23. add onKick function in members-modal.tsx file.
```
const onKick = async (memberId: string) => {
		try {
			setLoadingId(memberId)
			const url = qs.stringifyUrl({
				url: `/api/members/${memberId}`,
				query: {
					serverId: server?.id
				}
			})

			const response = await axios.delete(url);


			router.refresh();
			onOpen("members", {server: response.data})

		} catch (error) {
			console.log(error)
		} finally {
			setLoadingId("")
		}
	}
```
24. Add onClick function to Kick tag
```
<DropdownMenuItem
    onClick={() => onKick(member.id)}
>
    <Gavel className="h-4 w-4 mr-2" />
    Kick
</DropdownMenuItem>
```

## Channel Creation

1. Add "createChannel" in the use-modal-store file.
2. create a file in components/modals named create-channel-modal.tsx
3. add component to modal-provider.tsx file.
4. Go to server-header.tsx file and add onClick function on Create channel tag.
5. Below mentioned code the initial code for create-channel-modal.tsx
```
"use client";

import * as z from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import axios from "axios";

import {
	Dialog,
	DialogFooter,
	DialogHeader,
	DialogTitle,
	DialogContent,
} from "@/components/ui/dialog";
import {
	Form,
	FormControl,
	FormField,
	FormItem,
	FormLabel,
	FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";


import { useRouter } from "next/navigation";
import { useModal } from "@/hooks/use-modal-store";

const formSchema = z.object({
	name: z.string().min(1, {
		message: "Server name is required.",
	})
});

export const CreateChannelModal = () => {
	const { isOpen, onClose, type } = useModal();

	const router = useRouter();

	const isModalOpen = isOpen && type === "createChannel";

	const form = useForm({
		resolver: zodResolver(formSchema),
		defaultValues: {
			name: "",
		},
	});

	const isLoading = form.formState.isSubmitting;

	const onSubmit = async (values: z.infer<typeof formSchema>) => {
		try {
			await axios.post("/api/servers", values);

			form.reset();
			router.refresh();
			onClose();
		} catch (error) {
			console.log(error);
		}
	};

	const handleClose = () => {
		form.reset();
		onClose();
	};

	return (
		<Dialog open={isModalOpen} onOpenChange={handleClose}>
			<DialogContent className="bg-white text-black p-0 overflow-hidden">
				<DialogHeader className="pt-8 px-6">
					<DialogTitle className="text-2xl text-center font-bold">
						Create Channel
					</DialogTitle>
				</DialogHeader>
				<Form {...form}>
					<form
						onSubmit={form.handleSubmit(onSubmit)}
						className="space-y-8"
					>
						<div className="space-y-8 px-6">

							<FormField
								control={form.control}
								name="name"
								render={({ field }) => (
									<FormItem>
										<FormLabel className="uppercase text-xs font-bold text-zinc-500 dark:text-secondary/70">
											Channel name
										</FormLabel>
										<FormControl>
											<Input
												disabled={isLoading}
												className="bg-zinc-300/50 border-0 focus-visible:ring-0 text-black focus-visible:ring-offset-0"
												placeholder="Enter channel name"
												{...field}
											/>
										</FormControl>
										<FormMessage />
									</FormItem>
								)}
							/>
						</div>
						<DialogFooter className="bg-gray-100 px-6 py-4">
							<Button variant="primary" disabled={isLoading}>
								Create
							</Button>
						</DialogFooter>
					</form>
				</Form>
			</DialogContent>
		</Dialog>
	);
};

```
6. So now we have to add a component from shadcn ui which is going to enable us to pick the type of new create channel because channel can be of many types.
7. npx shadcn-ui@latest add select
8. add type in the form, add select field in the form, make channel type TEXT by defualt in the form.
9. After adding the form control we have to take care of a filter of the channel to solve this problem we have to use query string library.
10. The final code for app/api/channels/routes.ts file.
```
import { currentProfile } from "@/lib/current-profile"
import { db } from "@/lib/db";
import { MemberRole } from "@prisma/client";
import { NextResponse } from "next/server"

export async function POST(
    req: Request
) {
    try {
        const profile = await currentProfile();

        const {name, type} = await req.json()

        const { searchParams } = new URL(req.url);

        const serverId = searchParams.get("serverId")

        if (!profile) {
            return new NextResponse("Unauthorized", {status: 401})
        }

        if (!serverId) {
            return new NextResponse("Server ID missing", {status: 400})
        }

        if (name === "general") {
            return new NextResponse("Name cannot be 'general'", {status: 400})
        }

        const server = await db.server.update({
            where: {
                id: serverId,
                members: {
                    some: {
                        profileId: profile.id,
                        role: {
                            in: [MemberRole.ADMIN, MemberRole.MODERATOR]
                        }
                    }
                }
            },
            data: {
                channels: {
                    create: {
                        profileId: profile.id,
                        name,
                        type
                    }
                }
            }

        })

        return NextResponse.json(server);


    } catch (error) {
        console.log("[CHANNELS_POST]", error)
        return new NextResponse("Internal Error", {status: 500})
    }
}
```

11. The final code for create-channel-modal.tsx file.
```
"use client";

import qs from "query-string";
import * as z from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import axios from "axios";

import {
	Dialog,
	DialogFooter,
	DialogHeader,
	DialogTitle,
	DialogContent,
} from "@/components/ui/dialog";
import {
	Form,
	FormControl,
	FormField,
	FormItem,
	FormLabel,
	FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";


import { useParams, useRouter } from "next/navigation";
import { useModal } from "@/hooks/use-modal-store";
import {
    SelectContent,
    Select,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import { ChannelType } from "@prisma/client";



const formSchema = z.object({
	name: z.string().min(1, {
		message: "Channel name is required.",
	}).refine(
        name => name !== "general", 
        {
            message: "Channel name cannot be 'general'"
        }
    ),
    type: z.nativeEnum(ChannelType)
});

export const CreateChannelModal = () => {
	const { isOpen, onClose, type } = useModal();

	const router = useRouter();
    const params = useParams();

	const isModalOpen = isOpen && type === "createChannel";

	const form = useForm({
		resolver: zodResolver(formSchema),
		defaultValues: {
			name: "",
            type: ChannelType.TEXT
		},
	});

	const isLoading = form.formState.isSubmitting;

	const onSubmit = async (values: z.infer<typeof formSchema>) => {
		try {
            const url = qs.stringifyUrl({
                url: "/api/channels",
                query: {
                    serverId: params?.serverId
                }
            })
			await axios.post(url, values);

			form.reset();
			router.refresh();
			onClose();
		} catch (error) {
			console.log(error);
		}
	};

	const handleClose = () => {
		form.reset();
		onClose();
	};

	return (
		<Dialog open={isModalOpen} onOpenChange={handleClose}>
			<DialogContent className="bg-white text-black p-0 overflow-hidden">
				<DialogHeader className="pt-8 px-6">
					<DialogTitle className="text-2xl text-center font-bold">
						Create Channel
					</DialogTitle>
				</DialogHeader>
				<Form {...form}>
					<form
						onSubmit={form.handleSubmit(onSubmit)}
						className="space-y-8"
					>
						<div className="space-y-8 px-6">

							<FormField
								control={form.control}
								name="name"
								render={({ field }) => (
									<FormItem>
										<FormLabel className="uppercase text-xs font-bold text-zinc-500 dark:text-secondary/70">
											Channel name
										</FormLabel>
										<FormControl>
											<Input
												disabled={isLoading}
												className="bg-zinc-300/50 border-0 focus-visible:ring-0 text-black focus-visible:ring-offset-0"
												placeholder="Enter channel name"
												{...field}
											/>
										</FormControl>
										<FormMessage />
									</FormItem>
								)}
							/>
                            <FormField
                                control={form.control}
                                name="type"
                                render={({field}) => (
                                    <FormItem>
                                        <FormLabel>Channel Type</FormLabel>
                                        <Select
                                            disabled={isLoading}
                                            onValueChange={field.onChange}
                                            defaultValue={field.value}
                                        >
                                            <FormControl>
                                                <SelectTrigger
                                                    className="bg-zinc-300/50 border-0 focus:ring-0 text-black ring-offset-0 focus:ring-offset-0 capitalize outline-none"
                                                >
                                                    <SelectValue
                                                        placeholder="Select a channel type"
                                                    />
                                                </SelectTrigger>
                                            </FormControl>
                                            <SelectContent>
                                                {Object.values(ChannelType).map((type) => (
                                                    <SelectItem
                                                        key={type}
                                                        value={type}
                                                        className="capitalize"
                                                    >
                                                        {type.toLowerCase()}
                                                    </SelectItem>
                                                ))}
                                            </SelectContent>
                                        </Select>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
						</div>
						<DialogFooter className="bg-gray-100 px-6 py-4">
							<Button variant="primary" disabled={isLoading}>
								Create
							</Button>
						</DialogFooter>
					</form>
				</Form>
			</DialogContent>
		</Dialog>
	);
};
```
## Delete and Leave server Modal

1. Lets first build leave server functionality.
2. make sure to have atleat 2 people in the same server and  having admin access and other having guest access.
3. add "leaverServer" in the use-modal-store.ts file.
4. create leave-server-modal.tsx file in components/modals folder.
5. add this file in the providers.
6. add onClick function on Leaver server tag in server-header.tsx file.
```
{!isAdmin && (
    <DropdownMenuItem
        onClick={() => onOpen("leaveServer", {server})}
        className="text-rose-500 px-3 py-2 text-sm cursor-pointer"
        >
        Leave Server
        <LogOut className="h-4 w-4 ml-auto" />
    </DropdownMenuItem>
)}
```
7. The structure of leave-server-modal.tsx file is represent below.
```
"use client";

import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import {
	Dialog,
	DialogHeader,
	DialogTitle,
	DialogContent,
    DialogDescription,
    DialogFooter,
} from "@/components/ui/dialog";
import { useModal } from "@/hooks/use-modal-store";
import { Button } from "@/components/ui/button";


export const LeaveServerModal = () => {
	const { isOpen, onClose, type, data } = useModal();
    const router = useRouter();

	const isModalOpen = isOpen && type === "leaveServer";
	const { server } = data;
	const [isLoading, setIsLoading] = useState(false);


    const onClick = async () => {
        try {
            setIsLoading(true)

            await axios.patch(`/api/servers/${server?.id}/leave`)
            onClose();
            router.refresh();
            router.push("/")

        } catch (error) {
            console.log(error)
        } finally {
            setIsLoading(false)
        }
    }

	return (
		<Dialog open={isModalOpen} onOpenChange={onClose}>
			<DialogContent className="bg-white text-black p-0 overflow-hidden">
				<DialogHeader className="pt-8 px-6">
					<DialogTitle className="text-2xl text-center font-bold">
						Leave Server
					</DialogTitle>
					<DialogDescription className="text-center text-zinc-500">
						Are you sure you want to leave{" "}
						<span className="font-semibold text-indigo-500">
							{server?.name}
						</span>
						?
					</DialogDescription>
				</DialogHeader>
				<DialogFooter className="bg-gray-100 px-6 py-4">
					<div className="flex items-center justify-between w-full">
						<Button
							disabled={isLoading}
							onClick={onClose}
							variant="ghost"
						>
							Cancel
						</Button>
						<Button
							disabled={isLoading}
							variant="primary"
							onClick={onClick}
						>
							Confirm
						</Button>
					</div>
				</DialogFooter>
			</DialogContent>
		</Dialog>
	);
};

```
8. create a route.ts file in api/servers/[serverId]/leave/route.ts.
9. Now we have to create Delete server Modal which is kind of similar.
10. add "deleteServer" in the use-modal-store.ts file.
11. create delete-server-modal.tsx file in components/modals.
12. add this component to modal-provider.tsx file.
13. add an onClick function on Delete server tag in server-header.tsx file.
```
{isAdmin && (
    <DropdownMenuItem
        onClick={() => onOpen("deleteServer", { server })}
        className="text-rose-500 px-3 py-2 text-sm cursor-pointer"
    >
        Delete Server
        <Trash className="h-4 w-4 ml-auto" />
    </DropdownMenuItem>
)}
```
14. Structure of delete-server-modal.tsx file.
```
"use client";

import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import {
	Dialog,
	DialogHeader,
	DialogTitle,
	DialogContent,
	DialogDescription,
	DialogFooter,
} from "@/components/ui/dialog";
import { useModal } from "@/hooks/use-modal-store";
import { Button } from "@/components/ui/button";

export const DeleteServerModal = () => {
	const { isOpen, onClose, type, data } = useModal();
	const router = useRouter();

	const isModalOpen = isOpen && type === "deleteServer";
	const { server } = data;
	const [isLoading, setIsLoading] = useState(false);

	const onClick = async () => {
		try {
			setIsLoading(true);

			await axios.delete(`/api/servers/${server?.id}`);
			onClose();
			router.refresh();
			router.push("/");
		} catch (error) {
			console.log(error);
		} finally {
			setIsLoading(false);
		}
	};

	return (
		<Dialog open={isModalOpen} onOpenChange={onClose}>
			<DialogContent className="bg-white text-black p-0 overflow-hidden">
				<DialogHeader className="pt-8 px-6">
					<DialogTitle className="text-2xl text-center font-bold">
						Delete Server
					</DialogTitle>
					<DialogDescription className="text-center text-zinc-500">
						Are you sure you want to do this? <br />
						<span className="text-indigo-500 font-semibold">{server?.name}</span> will be permanently deleted.
						
					</DialogDescription>
				</DialogHeader>
				<DialogFooter className="bg-gray-100 px-6 py-4">
					<div className="flex items-center justify-between w-full">
						<Button
							disabled={isLoading}
							onClick={onClose}
							variant="ghost"
						>
							Cancel
						</Button>
						<Button
							disabled={isLoading}
							variant="primary"
							onClick={onClick}
						>
							Confirm
						</Button>
					</div>
				</DialogFooter>
			</DialogContent>
		</Dialog>
	);
};

```
15. add a new route in api/servers/[serverId]/route.ts file and the code of the function is given below.

```
export async function DELETE(
	req: Request,
	{ params }: { params: { serverId: string } }
) {
	try {
		const profile = await currentProfile();

		if (!profile) {
			return new NextResponse("Unauthorized", { status: 404 });
		}

		const server = await db.server.delete({
			where: {
				id: params.serverId,
				profileId: profile.id,
			}
		});

		return NextResponse.json(server);
	} catch (error) {
		console.log("[SERVER_ID_DELETE]", error);
		return new NextResponse("Internal Error", { status: 500 });
	}
}
```

