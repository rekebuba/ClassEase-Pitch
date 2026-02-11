import { useState } from "react";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

import LoginTab from "./tab/login-tab";
import SignupTab from "./tab/signup-tab";

function AuthActionBar() {
  const [activeTab, setActiveTab] = useState("login");

  return (
    <Tabs value={activeTab} onValueChange={setActiveTab}>
      <TabsList className="grid w-full grid-cols-2">
        <TabsTrigger value="login">
          <a href="#login">Log In</a>
        </TabsTrigger>
        <TabsTrigger value="signup">
          <a href="#signup">Sign Up</a>
        </TabsTrigger>
      </TabsList>
      <TabsContent value="login" id="login">
        <LoginTab setActiveTab={setActiveTab} />
      </TabsContent>
      <TabsContent value="signup" id="signup">
        <SignupTab />
      </TabsContent>
    </Tabs>
  );
}

export default AuthActionBar;
