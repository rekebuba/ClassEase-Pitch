const DateDisplay = () => {
  const date = new Date();
  const week = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday"
  ];

  return (
    <figure className="w-32 h-[111px] bg-white relative mx-auto my-[30px] rounded-[10px] before:content-[''] before:block before:w-32 before:h-[69px] before:bg-[-webkit-linear-gradient(white_0%,#edeeef_100%)] before:bg-[linear-gradient(white_0%,#edeeef_100%)] before:rounded-[10px_10px_0_0]">
      <header
        style={{ font: "400 15px/27px Arial, Helvetica, Geneva, sans-serif" }}
        className="w-32 h-[27px] absolute bg-[#fa565a] border-b-neutral-200 tracking-[0.5px] text-white text-center rounded-[10px_10px_0_0] border-b-[3px] border-solid -top-px"
      >
        {week[date.getDay()]}
      </header>
      <section className="w-32 h-20 absolute tracking-[-2px] text-[#4c566b] text-center z-10 top-7 before:content-[''] before:block before:absolute before:w-[3px] before:h-2.5 before:bg-[-moz-linear-gradient(#b5bdc5_0%,#e5e5e5_100%)] before:bg-[linear-gradient(#b5bdc5_0%,#e5e5e5_100%)] before:top-[35px] after:content-[''] after:block after:absolute after:w-[3px] after:h-2.5 after:bg-[-moz-linear-gradient(#b5bdc5_0%,#e5e5e5_100%)] after:bg-[linear-gradient(#b5bdc5_0%,#e5e5e5_100%)] after:right-0 after:top-[35px]">
        {date.getDate()}
      </section>
    </figure>
  );
};

export default DateDisplay;
