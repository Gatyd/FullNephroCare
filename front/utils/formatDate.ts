export default function formatDate(
    dateString: string, 
    month: "numeric" | "2-digit" | "long" | "short" | "narrow" | undefined = "long",
    datetime: boolean = true
) {
  const date = new Date(dateString);
  const options: Intl.DateTimeFormatOptions = {
    year: "numeric",
    month: month,
    day: "2-digit",
    hour: datetime ? "2-digit" : undefined,
    minute: datetime ? "2-digit" : undefined,
  };
  return date.toLocaleString("fr-FR", options);
}