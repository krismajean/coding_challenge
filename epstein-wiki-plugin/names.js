// List of people named in the Epstein files, mapped to their Wikipedia section anchors.
// Source: https://en.wikipedia.org/wiki/List_of_people_named_in_the_Epstein_files
//
// Each entry: { name: "Display Name", anchor: "Section_Anchor", aliases: [...optional] }
// The anchor corresponds to the heading ID on the Wikipedia article.

const WIKI_BASE_URL =
  "https://en.wikipedia.org/wiki/List_of_people_named_in_the_Epstein_files";

const EPSTEIN_NAMES = [
  // Politicians & Government Officials
  { name: "Bill Clinton", anchor: "Bill_Clinton" },
  { name: "Hillary Clinton", anchor: "Bill_Clinton", aliases: ["Hillary Rodham Clinton"] },
  { name: "Donald Trump", anchor: "Donald_Trump" },
  { name: "Jose Maria Aznar", anchor: "Jos%C3%A9_Mar%C3%ADa_Aznar", aliases: ["José María Aznar"] },
  { name: "Ehud Barak", anchor: "Ehud_Barak" },
  { name: "Miroslav Lajcak", anchor: "Miroslav_Laj%C4%8D%C3%A1k", aliases: ["Miroslav Lajčák"] },
  { name: "Sergey Lavrov", anchor: "Sergey_Lavrov" },
  { name: "Howard Lutnick", anchor: "Howard_Lutnick" },
  { name: "Jack Lang", anchor: "Jack_Lang" },
  { name: "Steve Bannon", anchor: "Steve_Bannon", aliases: ["Stephen Bannon"] },
  { name: "Vitaly Churkin", anchor: "Vitaly_Churkin" },
  { name: "Stacey Plaskett", anchor: "Stacey_Plaskett" },
  { name: "Ro Khanna", anchor: "Ro_Khanna" },

  // Royalty
  { name: "Prince Andrew", anchor: "Prince_Andrew", aliases: ["Andrew Mountbatten-Windsor", "Duke of York"] },
  { name: "Sarah Ferguson", anchor: "Sarah_Ferguson", aliases: ["Duchess of York"] },
  { name: "Mette-Marit", anchor: "Mette-Marit", aliases: ["Crown Princess Mette-Marit"] },

  // Business Leaders & Tech
  { name: "Bill Gates", anchor: "Bill_Gates", aliases: ["William Gates"] },
  { name: "Melinda French Gates", anchor: "Melinda_French_Gates", aliases: ["Melinda Gates"] },
  { name: "Elon Musk", anchor: "Elon_Musk" },
  { name: "Ronald Lauder", anchor: "Ronald_Lauder" },
  { name: "Leon Black", anchor: "Leon_Black" },
  { name: "Bobby Kotick", anchor: "Bobby_Kotick" },
  { name: "Marc Rowan", anchor: "Marc_Rowan" },
  { name: "Richard Branson", anchor: "Richard_Branson" },
  { name: "Les Wexner", anchor: "Les_Wexner", aliases: ["Leslie Wexner"] },
  { name: "Jeff Bezos", anchor: "Jeff_Bezos", aliases: ["Jeffrey Bezos"] },
  { name: "Sergey Brin", anchor: "Sergey_Brin" },
  { name: "Steve Tisch", anchor: "Steve_Tisch" },
  { name: "Casey Wasserman", anchor: "Casey_Wasserman" },
  { name: "Anil Ambani", anchor: "Anil_Ambani" },
  { name: "Sultan Ahmed bin Sulayem", anchor: "Sultan_Ahmed_bin_Sulayem" },
  { name: "Christopher Poole", anchor: "Christopher_Poole" },

  // Academics & Scientists
  { name: "Larry Summers", anchor: "Larry_Summers", aliases: ["Lawrence Summers"] },
  { name: "Peter Attia", anchor: "Peter_Attia" },
  { name: "Elisa New", anchor: "Elisa_New" },
  { name: "Boris Nikolic", anchor: "Boris_Nikolic" },
  { name: "Joscha Bach", anchor: "Joscha_Bach" },
  { name: "Stephen Kosslyn", anchor: "Stephen_Kosslyn" },
  { name: "Lawrence Krauss", anchor: "Lawrence_Krauss" },
  { name: "Dan Ariely", anchor: "Dan_Ariely" },
  { name: "Noam Chomsky", anchor: "Noam_Chomsky" },
  { name: "Stephen Hawking", anchor: "Stephen_Hawking" },
  { name: "Steven Pinker", anchor: "Steven_Pinker" },

  // Entertainment & Media
  { name: "Woody Allen", anchor: "Woody_Allen" },
  { name: "Michael Jackson", anchor: "Michael_Jackson" },
  { name: "Katie Couric", anchor: "Katie_Couric" },
  { name: "Kevin Spacey", anchor: "Kevin_Spacey" },
  { name: "David Copperfield", anchor: "David_Copperfield" },
  { name: "Martha Stewart", anchor: "Martha_Stewart" },
  { name: "Mick Jagger", anchor: "Mick_Jagger" },

  // Legal
  { name: "Alan Dershowitz", anchor: "Alan_Dershowitz" },
  { name: "Kathy Ruemmler", anchor: "Kathy_Ruemmler" },

  // Other Notable Figures
  { name: "Lynn Forester de Rothschild", anchor: "Lynn_Forester_de_Rothschild" },
  { name: "Caroline Lang", anchor: "Caroline_Lang" },
  { name: "Peter Listerman", anchor: "Peter_Listerman" },
  { name: "Peggy Siegal", anchor: "Peggy_Siegal" },

  // Inner Circle / Co-conspirators
  { name: "Ghislaine Maxwell", anchor: "Ghislaine_Maxwell" },
  { name: "Jean-Luc Brunel", anchor: "Jean-Luc_Brunel" },
  { name: "Jeffrey Epstein", anchor: "Jeffrey_Epstein" },
  { name: "Darren Indyke", anchor: "Darren_Indyke" },
  { name: "Richard Kahn", anchor: "Richard_Kahn" },
  { name: "Harry Beller", anchor: "Harry_Beller" },
  { name: "Lesley Groff", anchor: "Lesley_Groff" },
];
