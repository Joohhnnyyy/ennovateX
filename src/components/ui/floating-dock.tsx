/**
 * Note: Use position fixed according to your needs
 * Desktop navbar is better positioned at the bottom
 * Mobile navbar is better positioned at bottom right.
 **/

import { cn } from "@/lib/utils";
import { IconLayoutNavbarCollapse } from "@tabler/icons-react";
import { AnimatePresence, motion, useMotionValue, useSpring, useTransform, MotionValue } from "motion/react";

import { useRef, useState, useEffect } from "react";

export const FloatingDock = ({
  items,
  desktopClassName,
  mobileClassName
}: {
  items: {
    title: string;
    icon: React.ReactNode;
    href: string;
    onClick?: (e: React.MouseEvent) => void;
  }[];
  desktopClassName?: string;
  mobileClassName?: string;
}) => {
  const [isVisible, setIsVisible] = useState(false);
  const [mouseY, setMouseY] = useState(0);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      const windowHeight = window.innerHeight;
      const bottomThreshold = windowHeight * 0.8; // Show when cursor is in bottom 20% of screen
      
      setMouseY(e.clientY);
      
      // Only show dock when cursor approaches from bottom
      if (e.clientY > bottomThreshold) {
        setIsVisible(true);
      } else {
        // Hide dock when cursor moves away from bottom area
        setIsVisible(false);
      }
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <>
      <FloatingDockDesktop items={items} className={desktopClassName} isVisible={isVisible} />
      <FloatingDockMobile items={items} className={mobileClassName} isVisible={isVisible} />
    </>
  );
};

const FloatingDockMobile = ({
  items,
  className,
  isVisible
}: {
  items: {
    title: string;
    icon: React.ReactNode;
    href: string;
    onClick?: (e: React.MouseEvent) => void;
  }[];
  className?: string;
  isVisible: boolean;
}) => {
  const [open, setOpen] = useState(false);
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ 
        opacity: isVisible ? 1 : 0, 
        y: isVisible ? 0 : 20 
      }}
      transition={{ duration: 0.2, ease: "easeOut" }}
      className={cn("relative block md:hidden fixed bottom-4 left-1/2 transform -translate-x-1/2", className)}
      style={{ pointerEvents: isVisible ? 'auto' : 'none' }}>
      <AnimatePresence>
        {open && (
          <motion.div
            layoutId="nav"
            className="absolute inset-x-0 bottom-full mb-2 flex flex-col gap-2">
            {items.map((item, idx) => (
              <motion.div
                key={item.title}
                initial={{ opacity: 0, y: 10 }}
                animate={{
                  opacity: 1,
                  y: 0,
                }}
                exit={{
                  opacity: 0,
                  y: 10,
                  transition: {
                    delay: idx * 0.05,
                  },
                }}
                transition={{ delay: (items.length - 1 - idx) * 0.05 }}>
                <a
                  href={item.href}
                  key={item.title}
                  onClick={item.onClick}
                  className="flex h-10 w-10 items-center justify-center rounded-full bg-card/60 backdrop-blur-sm border border-border/30 hover:bg-primary/10 hover:border-primary/40 transition-all duration-200">
                  <div className="h-4 w-4">{item.icon}</div>
                </a>
              </motion.div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
      <button
        onClick={() => setOpen(!open)}
        className="flex h-10 w-10 items-center justify-center rounded-full bg-card/60 backdrop-blur-sm border border-border/30 hover:bg-primary/10 hover:border-primary/40 transition-all duration-200">
        <IconLayoutNavbarCollapse className="h-5 w-5 text-muted-foreground hover:text-primary transition-colors" />
      </button>
    </motion.div>
  );
};

const FloatingDockDesktop = ({
  items,
  className,
  isVisible
}: {
  items: {
    title: string;
    icon: React.ReactNode;
    href: string;
    onClick?: (e: React.MouseEvent) => void;
  }[];
  className?: string;
  isVisible: boolean;
}) => {
  let mouseX = useMotionValue(Infinity);
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ 
        opacity: isVisible ? 1 : 0, 
        y: isVisible ? 0 : 20 
      }}
      transition={{ duration: 0.2, ease: "easeOut" }}
      onMouseMove={(e) => mouseX.set(e.pageX)}
      onMouseLeave={() => mouseX.set(Infinity)}
      className={cn(
        "mx-auto hidden h-16 items-end gap-4 rounded-2xl bg-background/80 backdrop-blur-md border border-border/40 px-4 pb-3 md:flex shadow-lg fixed bottom-4 left-1/2 transform -translate-x-1/2",
        className
      )}
      style={{ pointerEvents: isVisible ? 'auto' : 'none' }}>
      {items.map((item) => (
        <IconContainer mouseX={mouseX} key={item.title} {...item} />
      ))}
    </motion.div>
  );
};

function IconContainer({
  mouseX,
  title,
  icon,
  href,
  onClick
}: {
  mouseX: MotionValue<number>;
  title: string;
  icon: React.ReactNode;
  href: string;
  onClick?: (e: React.MouseEvent) => void;
}) {
  let ref = useRef<HTMLDivElement>(null);

  let distance = useTransform(mouseX, (val: number) => {
    let bounds = ref.current?.getBoundingClientRect() ?? { x: 0, width: 0 };

    return val - bounds.x - bounds.width / 2;
  });

  let widthTransform = useTransform(distance, [-150, 0, 150], [40, 80, 40]);
  let heightTransform = useTransform(distance, [-150, 0, 150], [40, 80, 40]);

  let widthTransformIcon = useTransform(distance, [-150, 0, 150], [20, 40, 20]);
  let heightTransformIcon = useTransform(distance, [-150, 0, 150], [20, 40, 20]);

  let width = useSpring(widthTransform, {
    mass: 0.1,
    stiffness: 150,
    damping: 12,
  });
  let height = useSpring(heightTransform, {
    mass: 0.1,
    stiffness: 150,
    damping: 12,
  });

  let widthIcon = useSpring(widthTransformIcon, {
    mass: 0.1,
    stiffness: 150,
    damping: 12,
  });
  let heightIcon = useSpring(heightTransformIcon, {
    mass: 0.1,
    stiffness: 150,
    damping: 12,
  });

  const [hovered, setHovered] = useState(false);

  return (
    <a href={href} onClick={onClick}>
      <motion.div
        ref={ref}
        style={{ width, height }}
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
        className="relative flex aspect-square items-center justify-center rounded-full bg-card/60 backdrop-blur-sm border border-border/30 hover:bg-primary/10 hover:border-primary/40 transition-all duration-100">
        <AnimatePresence>
          {hovered && (
            <motion.div
              initial={{ opacity: 0, y: 10, x: "-50%" }}
              animate={{ opacity: 1, y: 0, x: "-50%" }}
              exit={{ opacity: 0, y: 2, x: "-50%" }}
              className="absolute -top-8 left-1/2 w-fit rounded-md border border-border bg-card/90 backdrop-blur-sm px-2 py-0.5 text-xs whitespace-pre text-foreground shadow-lg">
              {title}
            </motion.div>
          )}
        </AnimatePresence>
        <motion.div
          style={{ width: widthIcon, height: heightIcon }}
          className="flex items-center justify-center">
          {icon}
        </motion.div>
      </motion.div>
    </a>
  );
}