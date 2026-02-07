import { cva } from "class-variance-authority";

import { cn } from "@/lib/utils";

import type { VariantProps } from "class-variance-authority";
import type * as React from "react";

const shellVariants = cva("grid items-center gap-8 pt-6 pb-8 md:py-8", {
  variants: {
    variant: {
      default: "container",
      sidebar: "",
      centered: "container flex h-dvh max-w-2xl flex-col justify-center py-16",
      markdown: "container max-w-3xl py-8 md:py-10 lg:py-10",
    },
  },
  defaultVariants: {
    variant: "default",
  },
});

type ShellProps = {
  as?: React.ElementType;
} & React.HTMLAttributes<HTMLDivElement> & VariantProps<typeof shellVariants>;

function Shell({
  className,
  as: Comp = "section",
  variant,
  ...props
}: ShellProps) {
  return (
    <Comp className={cn(shellVariants({ variant }), className)} {...props} />
  );
}

export { Shell, shellVariants };
