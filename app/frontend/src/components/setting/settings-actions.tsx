import { RotateCcw, Save } from "lucide-react";

import { Button } from "@/components/ui/button";

type ActionFooterProps = {
  disabled?: boolean;
  saveLabel?: string;
};

export function ActionFooter({ disabled = false, saveLabel = "Save changes" }: ActionFooterProps) {
  return (
    <div className="sticky bottom-4 z-10 mt-6 flex flex-col gap-3 rounded-2xl border bg-background/95 p-3 shadow-lg backdrop-blur sm:flex-row sm:items-center sm:justify-between">
      <p className="text-sm text-muted-foreground">Static preview mode. Connect these actions to your backend when ready.</p>
      <div className="flex items-center gap-2">
        <Button variant="outline" disabled={disabled}>
          <RotateCcw className="size-4" />
          Reset
        </Button>
        <Button disabled={disabled}>
          <Save className="size-4" />
          {saveLabel}
        </Button>
      </div>
    </div>
  );
}
