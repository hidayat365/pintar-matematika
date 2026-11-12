"use strict";

const $ = (id) => document.getElementById(id);
const HURUF = ["A", "B", "C", "D"];
const KUNCI_AKTIF = "pintar.aktif";   // latihan yang sedang dikerjakan
const KUNCI_NAMA = "pintar.nama";

let topikTerpilih = null;
let aktif = null;        // {id, nama_topik, dibuat, soal, jawaban, posisi}
let detak = null;

// ------------------------------------------------------------------ bantuan

function simpan(kunci, nilai) {
  try {
    if (nilai === null) localStorage.removeItem(kunci);
    else localStorage.setItem(kunci, JSON.stringify(nilai));
  } catch (e) { /* penyimpanan browser tidak tersedia: abaikan */ }
}

function muat(kunci) {
  try { return JSON.parse(localStorage.getItem(kunci)); } catch (e) { return null; }
}

async function api(jalur, data) {
  const opsi = data === undefined ? {} : {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  };
  let res;
  try {
    res = await fetch(jalur, opsi);
  } catch (e) {
    throw new Error("Tidak bisa terhubung ke server. Pastikan server masih berjalan.");
  }
  const isi = await res.json().catch(() => ({}));
  if (!res.ok) {
    const galat = new Error(isi.galat || "Terjadi kesalahan.");
    galat.status = res.status;
    throw galat;
  }
  return isi;
}

function pesan(teks) {
  $("pesan").textContent = teks || "";
  $("pesan").hidden = !teks;
}

function aman(teks) {
  return String(teks).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

// Ubah "3/4" menjadi pecahan bersusun; teks lain di-escape dulu.
function matematika(teks) {
  return aman(teks).replace(/(\d+)\/(\d+)/g,
    '<span class="pecahan" aria-label="$1 per $2"><span>$1</span><span>$2</span></span>');
}

function jamMenit(detik) {
  const d = Math.max(0, Math.floor(detik));
  const m = Math.floor(d / 60);
  return `${String(m).padStart(2, "0")}:${String(d % 60).padStart(2, "0")}`;
}

function tanggal(iso) {
  const t = new Date(iso);
  if (isNaN(t)) return iso;
  return t.toLocaleString("id-ID", { day: "numeric", month: "short", year: "numeric",
    hour: "2-digit", minute: "2-digit" });
}

function predikat(nilai) {
  if (nilai >= 90) return { teks: "Luar biasa!", bintang: 3, kelas: "bagus" };
  if (nilai >= 75) return { teks: "Bagus sekali!", bintang: 2, kelas: "bagus" };
  if (nilai >= 60) return { teks: "Cukup baik", bintang: 1, kelas: "" };
  return { teks: "Ayo coba lagi!", bintang: 0, kelas: "kurang" };
}

function tampil(layar) {
  for (const s of document.querySelectorAll("main > section")) s.hidden = s.id !== `layar-${layar}`;
  for (const a of document.querySelectorAll("nav a")) {
    a.classList.toggle("aktif", a.dataset.nav === layar);
  }
  clearInterval(detak);
  window.scrollTo(0, 0);
}

// ------------------------------------------------------------------ beranda

async function bukaBeranda() {
  tampil("beranda");
  $("nama").value = muat(KUNCI_NAMA) || "";
  $("lanjut").hidden = !muat(KUNCI_AKTIF);
  if ($("daftar-topik").childElementCount) return;
  const { topik } = await api("/api/topik");
  for (const t of topik) {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "topik";
    b.setAttribute("role", "radio");
    b.setAttribute("aria-checked", "false");
    b.innerHTML = `<span class="ikon" aria-hidden="true">${aman(t.ikon)}</span>` +
      `<b>${aman(t.nama)}</b><small>${aman(t.ket)}</small>`;
    b.addEventListener("click", () => {
      topikTerpilih = t.kode;
      for (const x of $("daftar-topik").children) x.setAttribute("aria-checked", String(x === b));
      $("mulai").disabled = false;
    });
    $("daftar-topik").append(b);
  }
}

async function mulaiLatihan() {
  if (!topikTerpilih) return;
  if (muat(KUNCI_AKTIF) &&
      !confirm("Masih ada latihan yang belum selesai. Mulai latihan baru dan tinggalkan yang lama?")) return;
  $("mulai").disabled = true;
  try {
    const nama = $("nama").value.trim();
    simpan(KUNCI_NAMA, nama);
    const l = await api("/api/latihan", { nama, topik: topikTerpilih });
    aktif = { id: l.id, nama_topik: l.nama_topik, mulai: Date.now(), soal: l.soal,
      jawaban: l.soal.map(() => null), posisi: 0 };
    simpan(KUNCI_AKTIF, aktif);
    location.hash = "#/latihan";
  } catch (e) {
    pesan(e.message);
  } finally {
    $("mulai").disabled = false;
  }
}

// ------------------------------------------------------------------ latihan

function bukaLatihan() {
  aktif = aktif || muat(KUNCI_AKTIF);
  if (!aktif) { location.hash = "#/"; return; }
  tampil("latihan");
  $("l-topik").textContent = aktif.nama_topik;
  const perbarui = () => { $("l-waktu").textContent = "⏱ " + jamMenit((Date.now() - aktif.mulai) / 1000); };
  perbarui();
  detak = setInterval(perbarui, 1000);
  gambarSoal();
}

function gambarSoal() {
  const n = aktif.soal.length;
  const i = aktif.posisi;
  const s = aktif.soal[i];
  const terjawab = aktif.jawaban.filter((j) => j !== null).length;

  $("l-posisi").textContent = `Soal ${i + 1} dari ${n}`;
  $("l-batang").style.width = `${(terjawab / n) * 100}%`;
  $("l-teks").innerHTML = `${i + 1}. ${matematika(s.teks)}`;
  $("l-gambar").innerHTML = s.gambar || "";   // SVG buatan server sendiri
  $("l-gambar").hidden = !s.gambar;

  $("l-pilihan").replaceChildren(...s.pilihan.map((p, k) => {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "opsi";
    b.setAttribute("role", "radio");
    b.setAttribute("aria-checked", String(aktif.jawaban[i] === k));
    b.innerHTML = `<span class="huruf">${HURUF[k]}</span><span>${matematika(p)}</span>`;
    b.addEventListener("click", () => {
      aktif.jawaban[i] = k;
      simpan(KUNCI_AKTIF, aktif);
      gambarSoal();
    });
    return b;
  }));

  $("l-nomor").replaceChildren(...aktif.soal.map((_, k) => {
    const b = document.createElement("button");
    b.type = "button";
    b.textContent = k + 1;
    b.className = (aktif.jawaban[k] !== null ? "terjawab " : "") + (k === i ? "kini" : "");
    b.setAttribute("aria-label", `Soal ${k + 1}${aktif.jawaban[k] !== null ? ", sudah dijawab" : ", belum dijawab"}`);
    b.addEventListener("click", () => pindah(k));
    return b;
  }));

  $("l-sebelum").disabled = i === 0;
  $("l-berikut").disabled = i === n - 1;
}

function pindah(k) {
  aktif.posisi = Math.min(Math.max(k, 0), aktif.soal.length - 1);
  simpan(KUNCI_AKTIF, aktif);
  gambarSoal();
}

async function kumpulkan() {
  const kosong = aktif.jawaban.filter((j) => j === null).length;
  const tanya = kosong
    ? `Masih ada ${kosong} soal yang belum dijawab. Soal kosong dihitung salah. Tetap selesai?`
    : "Yakin sudah selesai? Jawaban tidak bisa diubah lagi.";
  if (!confirm(tanya)) return;
  const id = aktif.id;
  $("l-selesai").disabled = true;
  try {
    await api(`/api/latihan/${id}/jawab`, { jawaban: aktif.jawaban });
  } catch (e) {
    if (e.status !== 409 && e.status !== 404) {   // 409: sudah dikumpulkan → tampilkan hasilnya
      pesan(e.message);
      $("l-selesai").disabled = false;
      return;
    }
  }
  $("l-selesai").disabled = false;
  aktif = null;
  simpan(KUNCI_AKTIF, null);
  location.hash = `#/hasil/${id}`;
}

// -------------------------------------------------------------------- hasil

async function bukaHasil(id) {
  const h = await api(`/api/latihan/${id}`);
  if (!h.selesai) { location.hash = "#/"; return; }
  tampil("hasil");
  const p = predikat(h.nilai);
  $("h-bintang").textContent = "⭐".repeat(p.bintang);
  $("h-predikat").textContent = p.teks;
  $("h-nilai").textContent = h.nilai;
  $("h-nilai").className = "nilai-bulat " + p.kelas;
  $("h-info").textContent = `${h.nama} · ${h.nama_topik} · ${tanggal(h.selesai)}`;
  $("h-rinci").innerHTML = `Benar <b>${h.benar}</b> · Salah <b>${h.jumlah - h.benar}</b> · ` +
    `Waktu <b>${jamMenit(h.durasi)}</b>`;

  $("h-daftar").replaceChildren(...h.soal.map((s, i) => {
    const benar = s.jawaban === s.benar;
    const li = document.createElement("li");
    li.className = benar ? "benar" : "salah";
    const jawabanmu = s.jawaban === null ? "tidak dijawab"
      : `${HURUF[s.jawaban]}. ${matematika(s.pilihan[s.jawaban])}`;
    li.innerHTML =
      `<p class="tanya">${i + 1}. ${matematika(s.teks)}</p>` +
      (s.gambar ? `<div class="gambar kecil">${s.gambar}</div>` : "") +
      `<p><span class="lencana ${benar ? "benar" : "salah"}">${benar ? "✔ Benar" : "✘ Salah"}</span> ` +
      `Jawabanmu: <b>${jawabanmu}</b></p>` +
      (benar ? "" : `<p>Jawaban benar: <b>${HURUF[s.benar]}. ${matematika(s.pilihan[s.benar])}</b></p>`) +
      `<p class="penjelasan">💡 ${matematika(s.pembahasan)}</p>`;
    return li;
  }));
}

// ------------------------------------------------------------------ riwayat

async function bukaRiwayat() {
  const { ringkasan, latihan } = await api("/api/riwayat");
  tampil("riwayat");
  $("r-jumlah").textContent = ringkasan.jumlah;
  $("r-rata").textContent = ringkasan.rata_rata ?? "–";
  $("r-terbaik").textContent = ringkasan.terbaik ?? "–";
  $("r-kosong").hidden = latihan.length > 0;
  $("r-bungkus").hidden = latihan.length === 0;
  $("r-isi").replaceChildren(...latihan.map((l) => {
    const tr = document.createElement("tr");
    tr.innerHTML =
      `<td>${aman(tanggal(l.selesai))}</td><td>${aman(l.nama)}</td><td>${aman(l.nama_topik)}</td>` +
      `<td>${l.benar}/${l.jumlah}</td><td class="angka">${l.nilai}</td><td>${jamMenit(l.durasi)}</td>` +
      `<td><a href="#/hasil/${l.id}" aria-label="Lihat hasil latihan ${aman(l.nama)}">Lihat ▶</a></td>`;
    tr.addEventListener("click", () => { location.hash = `#/hasil/${l.id}`; });
    return tr;
  }));
}

// ------------------------------------------------------------------- rute

async function rute() {
  pesan("");
  const h = location.hash.replace(/^#\/?/, "");
  try {
    const hasil = h.match(/^hasil\/(\d+)$/);
    if (hasil) await bukaHasil(hasil[1]);
    else if (h === "latihan") bukaLatihan();
    else if (h === "riwayat") await bukaRiwayat();
    else await bukaBeranda();
  } catch (e) {
    tampil("beranda");
    pesan(e.message);
  }
}

$("mulai").addEventListener("click", mulaiLatihan);
$("l-sebelum").addEventListener("click", () => pindah(aktif.posisi - 1));
$("l-berikut").addEventListener("click", () => pindah(aktif.posisi + 1));
$("l-selesai").addEventListener("click", kumpulkan);
window.addEventListener("hashchange", rute);
rute();
