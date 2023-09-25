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
12. 






