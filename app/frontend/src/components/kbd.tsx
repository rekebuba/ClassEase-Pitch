import { cva } from "class-variance-authority";
import * as React from "react";

import { cn } from "@/lib/utils";

import type { VariantProps } from "class-variance-authority";

const kbdVariants = cva(
  "select-none rounded border px-1 py-px font-mono text-[0.7rem] font-normal shadow-sm disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-accent text-accent-foreground",
        outline: "bg-background text-foreground",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  },
);

export type KbdProps = {
  /**
   * The title of the `abbr` element inside the `kbd` element.
   * @default undefined
   * @type string | undefined
   * @example title="Command"
   */
  abbrTitle?: string;
} & React.ComponentPropsWithoutRef<"kbd"> & VariantProps<typeof kbdVariants>;

function Kbd({ ref, abbrTitle, children, className, variant, ...props }: KbdProps & { ref?: React.RefObject<HTMLUnknownElement | null> }) {
  return (
    <kbd
      className={cn(kbdVariants({ variant, className }))}
      ref={ref}
      {...props}
    >
      {abbrTitle
        ? (
            <abbr title={abbrTitle} className="no-underline">
              {children}
            </abbr>
          )
        : (
            children
          )}
    </kbd>
  );
}
Kbd.displayName = "Kbd";

export { Kbd };
