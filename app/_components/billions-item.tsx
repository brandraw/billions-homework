import { PhotoIcon } from "@heroicons/react/24/solid";
import Image from "next/image";
import Link from "next/link";

interface billionProps {
  id: string;
  name: string;
  squareImage: string;
  industries: string[];
  netWorth: number;
}

export default function BillionsItem({
  id,
  name,
  squareImage,
  industries,
  netWorth,
}: billionProps) {
  return (
    <Link href={`/person/${id}`} className="flex flex-col gap-2">
      <div className="relative aspect-square flex items-center justify-center border border-neutral-400 rounded-lg">
        <PhotoIcon className="size-10 text-neutral-400" />
        {/* <Image fill src={squareImage} alt={name} /> */}
      </div>
      <div className="flex flex-col gap-1">
        <h2 className="text-lg font-bold">{name}</h2>
        <div className="flex gap-1">
          {industries.map((a, i) => (
            <span key={i}>{a}</span>
          ))}
        </div>
      </div>
    </Link>
  );
}
