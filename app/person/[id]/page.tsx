import { formatToNumber } from "@/lib/util";
import { PhotoIcon } from "@heroicons/react/24/solid";
import Image from "next/image";

async function getPerson(name: string) {
  const result = await fetch(
    `https://billions-api.nomadcoders.workers.dev/person/${name}`
  );

  return await result.json();
}

export default async function PersonDetail({
  params: { id },
}: {
  params: { id: string };
}) {
  const person = await getPerson(id);
  console.log(person);

  return (
    <div className="py-14">
      <div className="max-w-screen-lg w-full mx-auto px-5 space-y-10">
        <div className="flex flex-col gap-2">
          <div className="relative aspect-square flex items-center justify-center border border-neutral-400 rounded-lg max-w-80">
            {/* <Image fill src={person.thumbnail} alt={person.name} /> */}
            <PhotoIcon className="size-10 text-neutral-400" />
          </div>
          <h1 className="text-2xl font-bold">{person.name}</h1>
          <span>Country: {person.country}</span>
          <span>Industry: {person.industries[0]}</span>
          <p>
            {person.bio.map((a: any) => (
              <>{a}</>
            ))}
          </p>
        </div>

        <div className="flex flex-col gap-5">
          <h2 className="text-2xl font-bold">Financial Assets</h2>
          <div className="grid grid-cols-4 gap-4">
            {person.financialAssets.map((a: any, i: number) => (
              <div
                className="border rounded-lg p-4 flex flex-col gap-1"
                key={i}
              >
                <span>Ticker: {a.ticker}</span>
                <span>Shares: {formatToNumber(a.numberOfShares)}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
