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
23. To take the full experience we need to write the command in the second terminal 
```
npx prisma studio
``` 
it will open a dashboard where i can see all the db tables and details.
24. Here we can see we have only one user and even after refresh it is not creating duplicate user.

## Initial Modal UI

1.  Now we have to create a modal for the ui.
