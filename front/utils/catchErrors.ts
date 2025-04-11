export default function catchErrors(err: any, toast: any) {
  let errMsg = "Erreur du serveur, réessayer plus tard";
  console.log(err);
  if (err.response) {
    const status = err.response.status;
    if (status >= 500) {
      toast.add({
        icon: "i-heroicons-exclamation-circle-20-solid",
        title: errMsg,
        color: "error",
      });
      return;
    }
  }
  const err_data = (err as any).data;
  if (typeof err_data === "object" && err_data !== null) {
    console.log(err_data);
    for (const [key, value] of Object.entries(err_data)) {
      toast.add({
        icon: "i-heroicons-exclamation-circle-20-solid",
        title: key,
        description: value as string,
        color: "error",
      });
    }
  } else {
    toast.add({
      icon: "i-heroicons-exclamation-circle-20-solid",
      title: errMsg,
      color: "error",
    });
  }
}
